'''
This module hold the endpoints for the 
plc_data feature.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
'''

# Import system libs
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import custom libs
from . import schemas
from .. import models
from ..database import get_db
from ..crud import Tplcdata

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def get_protocol_defaults():
    ''' Get the list of DataSource protocols available.\n
    return `val_list` (JSONResponse): A `schemas.simpleList` object
    automatically parsed into an HTTP_OK response.\n
    '''
    val_list = Tplcdata.get_avail_protocols()
    
    if (val_list==None):
        m_name = "protocols"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_list)
# --------------------

# --------------------
def get_datasource_defaults(prot_name:str):
    ''' Get the list of DataSource information to use as placeholders.\n
    `prot_name` (str): Protocol name to ger defauts from.\n
    return `val_dict` (JSONResponse): A `schemas.dataSourceInfo` object
    automatically parsed into an HTTP_OK response.\n
    '''
    val_dict = Tplcdata.get_datasource_placeholder(prot_name)
    
    if (val_dict==None):
        m_name = f"datasource information for Protocol: '{prot_name}'"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    return(val_dict)
# --------------------

# --------------------
def create_datasource(datasource:schemas.dataSourceInfo, db:Session=Depends(get_db)):
    ''' Create an entry at in database to save this DataSource.\n
    `datasource` (schemas.dataSourceInfo): DataSource informations.\n
    return `created` (JSONResponse): A boolean automatically parser into
    a HTTP_OK response.\n
    '''
    val_ds = Tplcdata.create_datasource(db,datasource)

    if (val_ds==None):
        m_name = f"Data Source '{datasource.name}'"
        raise HTTPException(status_code=404, detail=f"Error creating {m_name}.")

    return(val_ds)
# --------------------