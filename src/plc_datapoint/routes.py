'''
This module hold the endpoints for the 
plc_datapoint feature\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
'''

# Import system libs
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# Import custom libs
from . import schemas
from ..database import get_db
from ..crud import Tdatapoint
from ..user_auth import routes as usr_routes


#######################################


# --------------------
def get_datapoint_defaults(prot_name:str, usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the list of DataPoint information to use as placeholders.\n
    `prot_name` (str): Protocol name to ger defauts from.\n
    return `val_dict` (JSONResponse): A `schemas.dataPointInfo` object
    automatically parsed into an HTTP_OK response.\n
    '''
    val_dict = Tdatapoint.get_datapoint_placeholder(prot_name)
    
    if (val_dict is None):
        m_name = f"datapoint information for Protocol: '{prot_name}'"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dict)
# --------------------

# --------------------
def create_datapoint(datapoint:schemas.dataPointInfo, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Create an entry at in database to save this DataPoint.\n
    `datapoint` (schemas.dataPointInfo): DataPoint informations.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    try:
        val_dp = Tdatapoint.create_datapoint(db,datapoint)
    except Exception as exc:
        msg = str(exc).split('\n')[0]
        raise HTTPException(status_code=520, detail=msg)

    if (val_dp is None):
        m_name = f"Data Point '{datapoint.name}'"
        raise HTTPException(status_code=404, detail=f"Error creating {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def get_datapoint_by_name(dp_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name.\n
    `dp_name` (str): DataPoint name.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.get_datapoint_by_name(db, dp_name)

    if (val_dp is None):
        m_name = f"Data Point '{dp_name}'"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def update_datapoint(datapoint:schemas.dataPointInfo, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name and update it's informations.\n
    `datapoint` (schemas.dataPointInfo): DataPoint informations.\n
    return `val_dp` (JSONResponse): A `schemas.datapoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.update_datapoint(db, datapoint)

    if (val_dp is None):
        m_name = f"Data Point '{datapoint.name}'"
        raise HTTPException(status_code=404, detail=f"Error updating {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def change_datapoint_active_status(dp_name:str, active:bool, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name and change it's activated state.\n
    `dp_name` (str): DataPoint name.\n
    `active` (bool): Active state.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.activate_datapoint(db, dp_name, active)

    if (val_dp is None):
        m_name = f"Data Point '{dp_name}'"
        raise HTTPException(status_code=404, detail=f"Error activating {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def confirm_datapoints(dp_name:str, pending:bool, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search the names in database and change their pending state to False.\n
    `dp_name` (str): DataPoint name.\n
    `pending` (bool): new value of pending.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.confirm_datapoint(db, dp_name, pending)

    if (val_dp is None):
        m_name = f"Data Point"
        raise HTTPException(status_code=404, detail=f"Error on {m_name} authorizations.")

    return(val_dp)
# --------------------

# --------------------
def get_datapoints(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datapoint entries in database.\n
    return `val_dp` (JSONResponse): A list of `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.get_datapoints(db)

    if (val_dp is None):
        m_name = f"Data Points"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def get_datapoints_pending(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datapoint that are pending in database.\n
    return `val_dp` (JSONResponse): A list of `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.get_datapoints_pending(db)

    if (val_dp is None):
        m_name = f"Data Points"
        raise HTTPException(status_code=404, detail=f"Error searching for pending {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def get_datapoints_active(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datapoint that are acrive in database.\n
    return `val_dp` (JSONResponse): A list of `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.get_datapoints_active(db)

    if (val_dp is None):
        m_name = f"Data Points"
        raise HTTPException(status_code=404, detail=f"Error searching for pending {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def get_datapoints_by_range(ini:int, end:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datapoint entries in database.\n
    `ini` (int): First query result to show. Starts at `1`.\n
    `end` (int): Last query result to show, inclusive. \n
    return `val_dp` (JSONResponse): A list of `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''

    if(ini<1):
        raise HTTPException(status_code=401, detail=f"Range parameter error. Minimun value for `ini` is `1`.")

    val_dp = Tdatapoint.get_datapoints_by_range(db,ini,end)

    if (val_dp is None):
        m_name = f"Data Points"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dp)
# --------------------

# --------------------
def del_datapoint_by_name(dp_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Delete the specified entry from database.\n
    `ds_name` (str): DataPoint name.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_dp = Tdatapoint.delete_datapoint(db, dp_name)

    if (val_dp is None):
        m_name = f"Data Point"
        raise HTTPException(status_code=404, detail=f"Error on {m_name} deletion.")

    return(val_dp)
# --------------------