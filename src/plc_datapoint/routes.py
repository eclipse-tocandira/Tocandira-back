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
