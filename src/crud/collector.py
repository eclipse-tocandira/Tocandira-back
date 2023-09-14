'''
This module holds the functions to
access the Collector Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from ..env import Enviroment as Env
from .. import models
from ..collector import schemas
from .datasource import Tdatasource


#######################################

class Tcollector:
    ''' Class with CRUD methods to access the Collector table.\n
    '''

    # --------------------
    @staticmethod
    def get_defaults():
        ''' Parse the Collector default values.\n
        return `col` (schemas.collectorCreate): Default collector information.\n
        '''
        
        default = Env.DEFAULTS['Collector']

        col = schemas.collectorCreate(
            ip=default['ip'],
            name=default['name'],
            ssh_port=default['ssh_port'],
            ssh_user=default['ssh_user'],
            opcua_port=default['opcua_port'],
            health_port=default['health_port'],
            update_period=default['update_period'],
            timeout=2,
            ssh_pass='',
        )

        return(col)
    # --------------------

    # --------------------
    @staticmethod
    def create(db: Session, col_data: schemas.collectorCreate):
        ''' Create a new entry in the database.\n
        `db` (Session): Database session instance.\n
        `col_data` (schemas.collectorInfo): New collector information.\n
        return `db_col` (models.Collector): The created collector data.\n
        '''

        db_col = models.Collector(
            ip=col_data.ip,
            name=col_data.name,
            ssh_port=col_data.ssh_port,
            ssh_user=col_data.ssh_user,
            ssh_pass=col_data.ssh_pass,
            opcua_port=col_data.opcua_port,
            health_port=col_data.health_port,
            valid=False,
            update_period=col_data.update_period,
            timeout=col_data.timeout)
        db.add(db_col)
        db.commit()
        db.refresh(db_col)

        return (db_col)
    # --------------------

    # --------------------
    @staticmethod
    def _parse_collector(db_col:models.Collector):
        ''' Parde DB Collector table item to corresponding schema.\n
        `db_col` (models.Collector): Collector table item.\n
        return `col` (schemas.collector): Parsed collector information.\n
        '''

        # Prepare answer
        col = schemas.collector (
            id=db_col.id,
            ip=db_col.ip,
            name=db_col.name,
            ssh_port=db_col.ssh_port,
            ssh_user=db_col.ssh_user,
            opcua_port=db_col.opcua_port,
            health_port=db_col.health_port,
            valid=db_col.valid,
            update_period=db_col.update_period,
            timeout=db_col.timeout
        )

        return(col)
    # --------------------

    # --------------------
    @staticmethod
    def get_all(db:Session):
        ''' Query the database to get all collectors ID.\n
        `db` (Session): Database session instance.\n
        return (Query): All result of the query.\n
        '''
        qry = db.query(models.Collector)

        return(qry.all())
    # --------------------

    # --------------------
    @staticmethod
    def get_by_id(db:Session, id:int):
        ''' Query the database for a specific id.\n
        `db` (Session): Database session instance.\n
        `id` (int): Collector id to search for.\n
        return `db_col` (models.Collector): The first result of the query.\n
        '''
        qry = db.query(models.Collector)
        db_col = qry.filter(models.Collector.id == id).first()

        return (db_col)
    # --------------------

    # --------------------
    @staticmethod
    def update(db: Session, id:int ,col_data: schemas.collectorCreate):
        ''' Update the entry in the database.\n
        `db` (Session): Database session instance.\n
        `col_data` (schemas.collector): Existing collector information.\n
        return `db_col` (models.Collector): The updated collector data.\n
        '''
        db_col = Tcollector.get_by_id(db,id)

        db_col.ip=col_data.ip
        db_col.name=col_data.name
        db_col.ssh_port=col_data.ssh_port
        db_col.opcua_port=col_data.opcua_port
        db_col.health_port=col_data.health_port
        db_col.ssh_user=col_data.ssh_user
        db_col.ssh_pass=col_data.ssh_pass
        db_col.valid=False
        db_col.update_period=col_data.update_period
        db_col.timeout=col_data.timeout

        db.commit()

        return (db_col)
    # --------------------

    # --------------------
    @staticmethod
    def validate(db:Session, id:int, valid:bool=True):
        ''' Description \n
        `db` (Session): Database session instance.\n
        `id` (int): Collector id to search for.\n
        `valid` (bool): The validation state.\n
        return `db_col` (models.Collector): The validated collector data.\n
        '''
        db_col = Tcollector.get_by_id(db,id)
        db_col.valid=valid

        db.commit()

        return(db_col)
    # --------------------

    # --------------------
    @staticmethod
    def delete_collector(db:Session, id:int):
        ''' Delete a collector.\n
        `db` (Session): Database access session.\n
        `id` (int): Collector id to search for.\n
        return `col_answer` (dict): Dictionary containing the id removed and the status.\n
        '''
        col_answer = {}
        
        col = Tcollector.get_by_id(db,id)

        if (col is not None):
            for ds in col.datasources:
                Tdatasource.delete_datasource(db,ds.name)
            # Remove from database
            db.delete(col)
            db.commit()
            
            col_answer[id] = True
        else:
            col_answer[id] = False

        return(col_answer)
    # --------------------