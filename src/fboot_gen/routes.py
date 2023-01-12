'''
This module hold the endpoints for the 
fboot generator feature\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
* pyfboot
'''

# Import system libs
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pyfboot.gateway import MonoGatewayProject


# Import custom libs
from ..database import get_db
from ..env import Enviroment as Env
from ..user_auth import routes as usr_routes
from ..crud.datapoint import Tdatapoint
from ..crud.datasource import Tdatasource

#######################################


# --------------------
def export_gateway(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Export active database entries as a Forte OPC-UA gateway fboot file.\n
    return `res` (JSONResponse): A `bool` automatically parser into
    a HTTP_OK response.\n
    '''
    res = False

    # Create the 4diac Gateway Project
    prj_4diac = MonoGatewayProject(cycle_time=int(Env.CYCLETIME))

    try:
        # Get active datasources
        ds_list = Tdatasource.get_datasources_active(db)
        for ds in ds_list:

            # Get the datapoints from this datasource
            dp_list = Tdatapoint.get_datapoints_from_datasource(db,ds.name)
            for dp in dp_list:
                
                # Filter datapoints for active ones
                if dp.active:
                    # Get specific informations
                    dp = Tdatapoint._get_datapoint_implementation(db,dp.access.name,dp.name)
                    dp = Tdatapoint._parse_datapoint(dp)
                    # Create communication blocks and associate them with an OPC variable
                    comFB = prj_4diac.build_comm_block(ds.dict(),dp.dict())
                    prj_4diac.addVariable(dp.name,comFB)

        # Write project
        if Env.FBOOT_SSH_IP=='localhost':
            # Locally
            prj_4diac.write_fboot(Env.FBOOT_FILEURL, overwrite=True)
        else:
            # Over SSH
            prj_4diac.write_fboot(Env.FBOOT_FILEURL, overwrite=True,
                host=Env.FBOOT_SSH_IP, port=int(Env.FBOOT_SSH_PORT),
                username=Env.FBOOT_SSH_USERNAME)

        # Return Status
        res = True

    except Exception as exc:
        msg = str(exc).split('\n')[0]
        msg = f'Unexpected Error Found: "{msg}"'
        raise HTTPException(status_code=520, detail=msg)

    return(res)
# --------------------
