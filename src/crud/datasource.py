'''
This module holds the functions to
access the DataSource Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from .. import models
from ..env import Enviroment as Env
from ..plc_datasource import schemas


#######################################

class Tdatasource:
    ''' Class with CRUD methods to access the DataSource table.\n
    '''
    
    # --------------------
    @staticmethod
    def get_avail_protocols():
        ''' Search in DEFAULTS for the listed Protocols.\n
        return (schemas.comboBox): All protocols.\n
        '''
        prot_avail = schemas.comboBox(defaultValue='',menuItems=list(Env.DEFAULTS['Protocol'].keys()))

        return(prot_avail)
    # --------------------

    # --------------------
    @staticmethod
    def get_datasource_placeholder(prot_name:str):
        ''' Search in DEFAULTS for the placeholders of a specific protocol.\n
        `prot_name` (str): Name of the Protocol to search.\n
        return (schemas.dataSourceInfo): The information to pré-fill the fields.\n
        '''
        info = None

        # Check for asked protocol in defaults
        if prot_name in Env.DEFAULTS['Protocol'].keys():
            this_prot = Env.DEFAULTS['Protocol'][prot_name]

            # Parse protocol specific information
            p_info = {}
            for key, val in this_prot['protocol'].items():
                if('valid' in val.keys()):
                    p_info[key] = schemas.comboBox(defaultValue=val['value'],menuItems=val['valid'])
                else:
                    p_info[key] = val['value']
            
            # Mount Datasource infromation structure
            info = schemas.dataSourceInfo(
                name=this_prot['name']['value'],
                plc_ip=this_prot['plc_ip']['value'],
                plc_port=int(this_prot['plc_port']['value']),
                cycletime=int(Env.CYCLETIME),
                timeout=int(this_prot['timeout']['value']),
                status=False,
                protocol=schemas.protocolInfo(name=prot_name, data=p_info)
            )

        return(info)
    # --------------------

    # --------------------
    @staticmethod
    def _parse_protocol(db_prot:models.Protocol):
        ''' Parde DB protocol table item to corresponding schema.\n
        `db_prot` (models.Protocol): Protocol table item.\n
        return `prot` (schemas.protocol): Parsed protocol information.\n
        '''
        
        # Tranlate protocol table to specific implementation
        prot_data = {}
        for prop, value in db_prot.__dict__.items():
            if (not prop.startswith('_') and 'id' not in prop and 'name'!=prop):
                prot_data[prop] = value

        # Prepare answer
        prot = schemas.protocol(
            id=db_prot.id,
            name=db_prot.name,
            data=prot_data)
            
        return(prot)
    # --------------------

    # --------------------
    @staticmethod
    def _parse_datasource(db_ds:models.DataSource,prot:schemas.protocol):
        ''' Parde DB datasource table item to corresponding schema.\n
        `db_ds` (models.DataSource): Datasource table item.\n
        `prot` (schemas.protocol): Protocol parsed information.\n
        return `ds` (schemas.dataSource): Parsed datasource information.\n
        '''

        # Prepare answer
        ds = schemas.dataSource(
            id=db_ds.id,
            name=db_ds.name,
            plc_ip=db_ds.plc_ip,
            plc_port=db_ds.plc_port,
            cycletime=db_ds.cycletime,
            timeout=db_ds.timeout,
            status=db_ds.status,
            protocol=prot
        )

        return(ds)
    # --------------------

    # --------------------
    @staticmethod
    def _find_datasource_prototol(db:Session, db_ds:models.DataSource):
        ''' Parde DB table to corresponding schema.\n
        `db` (Session): Database access session.\n
        `db_ds` (models.DataSource): Datasource table item.\n
        return `sb_prot` (models.Protocol): Corresponding protocol table item.\n
        '''
        # Get protocol infos
        p_id = db_ds.protocol.id
        p_name = db_ds.protocol.name
        # Search protocol Table
        prot_cls = models.IMPLEMENTED_PROT[p_name]
        prot = db.query(prot_cls).filter(prot_cls.id == p_id).first()

        return(prot)
    # --------------------

    # --------------------
    @staticmethod
    def create_protocol(db: Session, new_prot:schemas.protocolInfo, ds:models.DataSource):
        ''' Create a new protocol.\n
        `db` (Session): Database access session.\n
        `new_prot` (schemas.protocolInfo): Informations on the new
        connection procotocol.\n
        `ds` (models.DataSource): The datasource table item to associate the
        new protocol to.\n
        return `prot_created` (schemas.protocol): The created table item
        information.\n
        '''
        prot_created = None

        if new_prot.name in models.IMPLEMENTED_PROT.keys():
            # Look for protocol implementations
            prot_cls = models.IMPLEMENTED_PROT[new_prot.name]
            # Instanciate the selected protocol
            db_prot = prot_cls(name=new_prot.name, datasource=ds)
            
            # Fill specific properties
            for prop, value in new_prot.data.items():
                setattr(db_prot, prop, value)

            # Insert in database
            db.add(db_prot)
            db.commit()
            db.refresh(db_prot)

            # Prepare answer
            prot_created = Tdatasource._parse_protocol(db_prot)
            
        return(prot_created)
    # --------------------

    # --------------------
    @staticmethod
    def create_datasource(db: Session, new_ds: schemas.dataSourceInfo):
        ''' Create a new datasource with the corresponding protocol
        but without any datapoint associated with it.\n
        `db` (Session): Database access session.\n
        `new_ds` (schemas.dataSourceInfo): Informations on the new
        datasource to create.\n
        return `ds_created` (schemas.dataSource): The created table item
        information.\n
        '''
        ds_created = None

        if new_ds.protocol.name in models.IMPLEMENTED_PROT.keys():

            # Instanciate DataSource
            db_ds = models.DataSource( name=new_ds.name,
                plc_ip=new_ds.plc_ip, plc_port=new_ds.plc_port,
                cycletime=new_ds.cycletime, timeout=new_ds.timeout)

            # Insert in database
            db.add(db_ds)
            db.commit()
            db.refresh(db_ds)

            # Create the corresponding protocol
            prot_created = Tdatasource.create_protocol(db, new_ds.protocol, db_ds)
            # Parse information
            ds_created = Tdatasource._parse_datasource(db_ds, prot_created)
        
        return(ds_created)
    # --------------------

    # --------------------
    @staticmethod
    def get_datasources(db:Session):
        ''' Get all datasources.\n
        `db` (Session): Database access session.\n
        return `ds_answer` (list): List of datasources in database.\n
        '''
        ds_answer = []
        # Declare the query
        dbq = db.query(models.DataSource)

        # Get Datasource list
        for ds in dbq.all():
            prot = Tdatasource._find_datasource_prototol(db,ds)
            # Parse data
            ds_answer.append( Tdatasource._parse_datasource(ds, Tdatasource._parse_protocol(prot)) )
        
        return (ds_answer)
    # --------------------

    # --------------------
    @staticmethod
    def get_datasources_by_range(db:Session, ini:int, end:int):
        ''' Get all datasources.\n
        `db` (Session): Database access session.\n
        `ini` (int): First query result to show.\n
        `end` (int): Last query result to show.\n
        return `ds_answer` (list): List of datasources in database.\n
        '''
        ds_answer = []
        # Declare the query
        dbq = db.query(models.DataSource)

        # Get Datasource list
        for ds in dbq.offset(ini-1).limit(end).all():
            prot = Tdatasource._find_datasource_prototol(db,ds)
            # Parse data
            ds_answer.append( Tdatasource._parse_datasource(ds, Tdatasource._parse_protocol(prot)) )
        
        return (ds_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def get_datasource_by_name(db:Session, ds_name:str):
        ''' Search datasource by name.\n
        `db` (Session): Database access session.\n
        `ds_name` (str): DataSource name.\n
        return `ds_answer` (schemas.dataSource): Datasource found, `None` if
        not found.\n
        '''
        ds_answer = None

        # Declare the query
        dbq = db.query(models.DataSource)

        # Get specific Datasource
        ds = dbq.filter(models.DataSource.name == ds_name).first()
        if (ds is not None):
            prot = Tdatasource._find_datasource_prototol(db,ds)
            # Parse data
            ds_answer = Tdatasource._parse_datasource(ds, Tdatasource._parse_protocol(prot))
        
        return (ds_answer)
    # --------------------