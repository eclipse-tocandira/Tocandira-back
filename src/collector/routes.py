'''
This module hold the endpoints for the 
collector feature.\n
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
from ..crud import Tcollector
from ..user_auth import routes as usr_routes

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def get_collector(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the collector entry in database.\n
    return `parsed_col` (JSONResponse): The saved `schemas.collectorInfo` automatically parser into
    a HTTP_OK response.\n
    '''
    # NOTE: The fixed ID is by design, this table will have only one entry
    val_col = Tcollector.get_by_id(db,id=1)
    
    if (val_col is None):
        m_name = f"Collector data"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    parsed_col = Tcollector._parse_collector(val_col)
    return(parsed_col)
# --------------------

# --------------------
def update_collector(collector:schemas.collectorInfo, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Update the collector entry in the database.\n
    `collector` (schemas.collectorInfo): Collector informations.\n
    return `parsed_col` (JSONResponse): Updated data of `schemas.collectorInfo` automatically parser into
    a HTTP_OK response.\n
    '''
    # NOTE: The fixed ID is by design, this table will have only one entry
    val_col = Tcollector.update(db,collector, id=1)

    if (val_col is None):
        m_name = f"Collector data"
        raise HTTPException(status_code=404, detail=f"Error updating {m_name}.")

    parsed_col = Tcollector._parse_collector(val_col)
    return(parsed_col)
# --------------------
