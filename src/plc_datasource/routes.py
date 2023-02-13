'''
This module hold the endpoints for the 
plc_datasource feature.\n
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
from ..crud import Tdatasource
from ..user_auth import routes as usr_routes

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def get_protocol_defaults(usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the list of DataSource protocols available.\n
    return `val_list` (JSONResponse): A `schemas.comboBox` object
    automatically parsed into an HTTP_OK response.\n
    '''
    val_list = Tdatasource.get_avail_protocols()
    
    if (val_list is None):
        m_name = "protocols"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_list)
# --------------------

# --------------------
def get_datasource_defaults(prot_name:str, usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the list of DataSource information to use as placeholders.\n
    `prot_name` (str): Protocol name to ger defauts from.\n
    return `val_dict` (JSONResponse): A `schemas.dataSourceInfo` object
    automatically parsed into an HTTP_OK response.\n
    '''
    val_dict = Tdatasource.get_datasource_placeholder(prot_name)
    
    if (val_dict is None):
        m_name = f"datasource information for Protocol: '{prot_name}'"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dict)
# --------------------

# --------------------
def create_datasource(datasource:schemas.dataSourceInfo, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Create an entry at in database to save this DataSource.\n
    `datasource` (schemas.dataSourceInfo): DataSource informations.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    try:
        val_ds = Tdatasource.create_datasource(db,datasource)
    except Exception as exc:
        msg = str(exc).split('\n')[0]
        raise HTTPException(status_code=520, detail=msg)

    if (val_ds is None):
        m_name = f"Data Source '{datasource.name}'"
        raise HTTPException(status_code=404, detail=f"Error creating {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def get_datasource_by_name(ds_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name.\n
    `ds_name` (str): DataSource name.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.get_datasource_by_name(db, ds_name)

    if (val_ds is None):
        m_name = f"Data Source '{ds_name}'"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def update_datasource(datasource:schemas.dataSourceInfo, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name and update it's informations.\n
    `datasource` (schemas.dataSourceInfo): DataSource informations.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.update_datasource(db, datasource)

    if (val_ds is None):
        m_name = f"Data Source '{datasource.name}'"
        raise HTTPException(status_code=404, detail=f"Error updating {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def change_datasource_active_status(ds_name:str, active:bool, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search an entry in database with provided name and change it's activated state.\n
    `ds_name` (str): DataSource name.\n
    `active` (bool): Active state.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.activate_datasource(db, ds_name, active)

    if (val_ds is None):
        m_name = f"Data Source '{ds_name}'"
        raise HTTPException(status_code=404, detail=f"Error activating {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def confirm_datasources(ds_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search the names in database and change their pending state to False.\n
    `ds_name` (str): DataSource name.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.confirm_datasource(db, ds_name)

    if (val_ds is None):
        m_name = f"Data Source"
        raise HTTPException(status_code=404, detail=f"Error on {m_name} authorizations.")

    return(val_ds)
# --------------------

# --------------------
def get_datasources(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datasource entries in database.\n
    return `val_ds` (JSONResponse): A list of `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.get_datasources(db)

    if (val_ds is None):
        m_name = f"Data Sources"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def get_datasources_pending(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datasource that are pending in database.\n
    return `val_ds` (JSONResponse): A list of `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.get_datasources_pending(db)

    if (val_ds is None):
        m_name = f"Data Sources"
        raise HTTPException(status_code=404, detail=f"Error searching for pending {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def get_datasources_active(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datasource that are acrive in database.\n
    return `val_ds` (JSONResponse): A list of `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.get_datasources_active(db)

    if (val_ds is None):
        m_name = f"Data Sources"
        raise HTTPException(status_code=404, detail=f"Error searching for pending {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def get_datasources_by_range(ini:int, end:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all datasource entries in database.\n
    `ini` (int): First query result to show. Starts at `1`.\n
    `end` (int): Last query result to show, inclusive. \n
    return `val_ds` (JSONResponse): A list of `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''

    if(ini<1):
        raise HTTPException(status_code=401, detail=f"Range parameter error. Minimun value for `ini` is `1`.")

    val_ds = Tdatasource.get_datasources_by_range(db,ini,end)

    if (val_ds is None):
        m_name = f"Data Sources"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_ds)
# --------------------

# --------------------
def del_datasource_by_name(ds_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Delete the specified entry from database.\n
    `ds_name` (str): DataSource name.\n
    return `val_ds` (JSONResponse): A `schemas.dataSource` automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tdatasource.delete_datasource(db, ds_name)

    if (val_ds is None):
        m_name = f"Data Source"
        raise HTTPException(status_code=404, detail=f"Error on {m_name} deletion.")

    return(val_ds)
# --------------------