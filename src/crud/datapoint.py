'''
This module holds the functions to
access the DataPoint Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from .. import models
from ..env import Enviroment as Env
from ..plc_datapoint import schemas
from ..plc_datasource import schemas as ds_schemas


#######################################

class Tdatapoint:
    ''' Class with CRUD methods to access the DataPoint table.\n
    '''
    
    # --------------------
    @staticmethod
    def get_datapoint_placeholder(prot_name:str):
        ''' Search in DEFAULTS for the placeholders of a specific protocol.\n
        `prot_name` (str): Name of the Protocol to search.\n
        return (schemas.dataPointInfo): The information to pré-fill the fields.\n
        '''
        info = None

        # Check for asked protocol in defaults
        if prot_name in Env.DEFAULTS['Data'].keys():
            this_access = Env.DEFAULTS['Data'][prot_name]

            # Parse protocol specific information
            a_info = {}
            for key, val in this_access['access'].items():
                if('valid' in val.keys()):
                    a_info[key] = ds_schemas.comboBox(defaultValue=val['value'],menuItems=val['valid'])
                else:
                    a_info[key] = val['value']
            
            # Mount Datapoint information structure
            info = schemas.dataPointInfo(
                name=this_access['name']['value'],
                description=this_access['description']['value'],
                num_type=ds_schemas.comboBox(defaultValue=this_access['num_type']['value'],menuItems=this_access['num_type']['valid']),
                datasource_name=this_access['datasource_name']['value'],
                access=schemas.accessInfo(name=prot_name,data=a_info)
            )

        return(info)
    # --------------------

    # --------------------
    @staticmethod
    def _find_datasource(db:Session, ds_name:str):
        ''' Search DB table for corresponding name.\n
        `db` (Session): Database access session.\n
        `ds_name` (str): Datasource table key.\n
        return `ds` (models.Datasource): Corresponding Datasource table item.\n
        '''
        # Declare the query
        dbq = db.query(models.DataSource)
        # Get specific Datasource
        ds = dbq.filter(models.DataSource.name == ds_name).first()
        
        return(ds)
    # --------------------

    # --------------------
    @staticmethod
    def _get_datapoint_implementation(db:Session, p_name:str, dp_name:str):
        ''' Search DB table for corresponding name.\n
        `db` (Session): Database access session.\n
        `gen_dp` (models.DataPoint): Datapoint table item.\n
        return `dp`: The Datapoint object but in the specific implementation.\n
        '''
        dp = None

        if p_name in models.IMPLEMENTED_DATA.keys():
            data_cls = models.IMPLEMENTED_DATA[p_name]
            # Declare the query
            dbq = db.query(data_cls)
            # Get specific Datasource
            dp = dbq.filter(data_cls.name == dp_name).first()
        
        return(dp)
    # --------------------

    # --------------------
    @staticmethod
    def _parse_datapoint(db_dp:models.DataPoint):
        ''' Parde DB datapoint table item to corresponding schema.\n
        `db_dp` (models.DataPoint): Datapoint table item.\n
        return `dp` (schemas.dataPoint): Parsed datapoint information.\n
        '''

        # Search in attributes for implementation specific parameters
        access_data = {}

        for prop in db_dp.__dict__.keys():
            if (not prop.startswith('_') and prop not in models.DataPoint.__dict__.keys()):
                access_data[prop] = getattr(db_dp,prop)
        
        # Prepare answer
        dp = schemas.dataPoint(
            name=db_dp.name,
            description=db_dp.description,
            num_type=db_dp.num_type,
            datasource_name=db_dp.datasource.name,
            access=schemas.accessInfo(name=db_dp.access,data=access_data),
            active=db_dp.active,
            pending=db_dp.pending,
            upload=db_dp.upload,
            # datasource=ds_info
        )

        return(dp)
    # --------------------

    # --------------------
    @staticmethod
    def create_datapoint(db: Session, new_dp: schemas.dataPointInfo):
        ''' Create a new datapoint with the corresponding protocol
        but without any datapoint associated with it.\n
        `db` (Session): Database access session.\n
        `new_dp` (schemas.dataPointInfo): Informations on the new
        datapoint to create.\n
        return `dp_created` (schemas.dataPoint): The created table item
        information.\n
        '''
        dp_created = None

        if new_dp.access.name in models.IMPLEMENTED_DATA.keys():

            data_cls = models.IMPLEMENTED_DATA[new_dp.access.name]
            ds = Tdatapoint._find_datasource(db,new_dp.datasource_name)
                
            if ds is not None:
                # Instanciate DataPoint
                db_dp = data_cls(
                    name=new_dp.name,
                    description=new_dp.description,
                    num_type=new_dp.num_type,
                    datasource=ds,
                    **new_dp.access.data)

                # Insert in database
                db.add(db_dp)
                db.commit()
                db.refresh(db_dp)
                
                # Parse information
                dp_created = Tdatapoint._parse_datapoint(db_dp)
        
        return(dp_created)
    # --------------------

    # --------------------
    def update_datapoint(db: Session, dp_update: schemas.dataPointInfo):
        ''' Search for a datapoints and update it's informations.\n
        `db` (Session): Database access session.\n
        `dp_update` (schemas.dataPointInfo): Informations on the new
        datapoint to create.\n
        return `dp_answer` (schemas.dataPoint): The modified datapoint.\n
        '''
        dp_answer = None

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_update.name).first()
        if (dp is not None):
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)

            # Update matching parameters in DataPoint
            for param, value in dp.__dict__.items():
                if (param in ['datasource','datasource_name','name','access']):
                    continue
                if param in dp_update.__dict__.keys():
                    value = getattr(dp_update,param)
                if param in dp_update.access.data.keys():
                    value = dp_update.access.data[param]
                setattr(dp,param,value)

            # Set validation to False 
            dp.pending = True
            # Parse data
            dp_answer = Tdatapoint._parse_datapoint(dp)
            
            # Insert changes in database
            db.commit()

        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def get_datapoints(db:Session):
        ''' Get all datapoints.\n
        `db` (Session): Database access session.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = []
        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get Datapoint list
        for dp in dbq.all():
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer.append( Tdatapoint._parse_datapoint(dp) )
        
        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def get_datapoints_by_range(db:Session, ini:int, end:int):
        ''' Get all datapoints.\n
        `db` (Session): Database access session.\n
        `ini` (int): First query result to show.\n
        `end` (int): Last query result to show.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = []
        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get Datapoint list
        for dp in dbq.offset(ini-1).limit(end).all():
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer.append( Tdatapoint._parse_datapoint(dp) )

        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def get_datapoints_pending(db:Session):
        ''' Get all datapoints that are pending.\n
        `db` (Session): Database access session.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = []
        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get Datapoint list
        for dp in dbq.filter(models.DataPoint.pending==True).all():
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer.append( Tdatapoint._parse_datapoint(dp) )

        return (dp_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def get_datapoints_active(db:Session):
        ''' Get all datapoints that are active.\n
        `db` (Session): Database access session.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = []
        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get Datapoint list
        for dp in dbq.filter(models.DataPoint.active==True).all():
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer.append( Tdatapoint._parse_datapoint(dp) )
        
        return (dp_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def confirm_datapoint(db:Session, dp_name:str, pending:bool):
        ''' Set specific data points as pending variable value pending.\n
        `db` (Session): Database access session.\n
        `dp_name` (str): DataPoint name.\n
        `pending` (bool): new value of pending.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = {}

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_name).first()
        if (dp is not None):
            # Insert in database
            dp.pending = pending
            db.commit()
            # Parse data
            dp_answer[dp_name] = True
        else:
            dp_answer[dp_name] = False
            
        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def confirm_upload_datapoint(db:Session, dp_name:str, upload:bool):
        ''' Set specific data points as pending variable value upload.\n
        `db` (Session): Database access session.\n
        `dp_name` (str): DataPoint name.\n
        `upload` (bool): new value of upload.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = {}

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_name).first()
        if (dp is not None):
            # Insert in database
            dp.upload = upload
            db.commit()
            # Parse data
            dp_answer[dp_name] = True
        else:
            dp_answer[dp_name] = False
            
        return (dp_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def get_datapoint_by_name(db:Session, dp_name:str):
        ''' Search datapoint by name.\n
        `db` (Session): Database access session.\n
        `dp_name` (str): DataPoint name.\n
        return `dp_answer` (schemas.dataPoint): Datapoint found, `None` if
        not found.\n
        '''
        dp_answer = None

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_name).first()
        if (dp is not None):
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer = Tdatapoint._parse_datapoint(dp)
        
        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def activate_datapoint(db:Session, dp_name:str, active:bool):
        ''' Set active state of a datapoint.\n
        `db` (Session): Database access session.\n
        `dp_name` (str): DataPoint names.\n
        `active` (bool): Activate state value.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = {}

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_name).first()
        if (dp is not None):
            # Insert in database
            dp.active = active
            db.commit()
            # Parse data
            dp_answer[dp_name] = True
        else:
            dp_answer[dp_name] = False
        
        return (dp_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def delete_datapoint(db:Session, dp_name:str):
        ''' Delete a datapoint.\n
        `db` (Session): Database access session.\n
        `dp_name` (str): DataPoint names.\n
        `active` (bool): Activate state value.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = {}

        # Declare the query
        dbq = db.query(models.DataPoint)

        # Get specific Datapoint
        dp = dbq.filter(models.DataPoint.name == dp_name).first()
        if (dp is not None):
            # Remove from database
            db.delete(dp)
            db.commit()
            # Parse data
            dp_answer[dp_name] = True
        else:
            dp_answer[dp_name] = False
        
        return (dp_answer)
    # --------------------
    
    # --------------------
    @staticmethod
    def get_datapoints_from_datasource(db:Session, ds_name:str):
        ''' Get all datapoints.\n
        `db` (Session): Database access session.\n
        `ds_name (str)`: DataSource name to search.\n
        return `dp_answer` (list): List of datapoints in database.\n
        '''
        dp_answer = []
        # Declare the query
        dbq = db.query(models.DataSource)
        # Get DataSource
        ds = dbq.filter(models.DataSource.name == ds_name).first()
        
        # Get Datapoint list
        for dp in ds.datapoints:
            # Get specific implementation of it
            dp = Tdatapoint._get_datapoint_implementation(db,dp.access,dp.name)
            # Parse data
            dp_answer.append( Tdatapoint._parse_datapoint(dp) )
        
        return (dp_answer)
    # --------------------

    # --------------------
    @staticmethod
    def get_datapoints_from_collector(db:Session, id:int):
        ''' Get all datapoints associated with a collector.\n
        `db` (Session): Database access session.\n
        `id` (int): Collector id to search for.\n
        return `dp_answer` (list): List of datapoints.\n
        '''
        dp_answer = []

        qry = db.query(models.Collector)
        col = qry.filter(models.Collector.id == id).first()

        if (col is not None):
            for ds in col.datasources:
                dp_answer += Tdatapoint.get_datapoints_from_datasource(db,ds.name)
        
        return(dp_answer)
    # --------------------