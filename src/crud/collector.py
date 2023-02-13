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
from .. import models
from ..collector import schemas


#######################################

class Tcollector:
    ''' Class with CRUD methods to access the Collector table.\n
    '''

    # --------------------
    @staticmethod
    def create(db: Session, col_data: schemas.collectorInfo):
        ''' Create a new entry in the database.\n
        `db` (Session): Database session instance.\n
        `col_data` (schemas.collectorInfo): New collector information.\n
        return `db_col` (models.Collector): The created collector data.\n
        '''

        db_col = models.Collector(
            ip=col_data.ip,
            port=col_data.port,
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
        return `col` (schemas.collectorInfo): Parsed collector information.\n
        '''

        # Prepare answer
        col = schemas.collectorInfo(
            ip=db_col.ip,
            port=db_col.port,
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
    def update(db: Session, col_data: schemas.collectorInfo, id:int):
        ''' Update the entry in the database.\n
        `db` (Session): Database session instance.\n
        `col_data` (schemas.collectorInfo): New collector information.\n
        `id` (int): Collector id to search for.\n
        return `db_col` (models.Collector): The updated collector data.\n
        '''
        db_col = Tcollector.get_by_id(db,id)

        db_col.ip=col_data.ip
        db_col.port=col_data.port
        db_col.update_period=col_data.update_period
        db_col.timeout=col_data.timeout

        db.commit()

        return (db_col)
    # --------------------
