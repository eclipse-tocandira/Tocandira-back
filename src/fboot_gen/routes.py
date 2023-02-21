'''
This module hold the endpoints for the 
fboot generator feature\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
* pyfboot
* fsspec
* pyyaml
'''

# Import system libs
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pyfboot.gateway import MonoGatewayProject
import fsspec
import yaml

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

    # Create OPCUA configuration file
    opcua_conf = { 'endPoint':Env.OPCUA_ENDPOINT, 'nodes':[] }

    try:
        # Get active datasources
        ds_list = Tdatasource.get_datasources_active(db)
        for ds in ds_list:
            # Filter datasources for confirmed ones
            if ds.pending:
                continue
            
            # Get the datapoints from this datasource
            dp_list = Tdatapoint.get_datapoints_from_datasource(db,ds.name)
            for dp in dp_list:
                
                # Filter datapoints for active ones
                if dp.active and not dp.pending:
                    # Get specific informations
                    dp = Tdatapoint._get_datapoint_implementation(db,dp.access.name,dp.name)
                    dp = Tdatapoint._parse_datapoint(dp)
                    # Create communication blocks and associate them with an OPC variable
                    comFB = prj_4diac.build_comm_block(ds.dict(),dp.dict())
                    prj_4diac.addVariable(dp.name,comFB)
                    # Create corresponding Node on OPCUA
                    opcua_conf['nodes'].append({
                        'nodeName':f'ns={1};s={dp.name}',
                        'metricName':f'{dp.name}',
                        'metricHelp':f'{dp.description}'
                    })

        # Insert one more node with the pre-defined observability variable
        opcua_conf['nodes'].append({
            'nodeName':'ns=1;s=_ForteCycleTime',
            'metricName':'_ForteCycleTime',
            'metricHelp':'Tempo de leitura das variavies do Forte'
        })

        protocol, _ = fsspec.core.split_protocol(Env.OPCUA_FILEURL)

        if protocol=='file':
            # Write Forte project
            prj_4diac.write_fboot(Env.FBOOT_FILEURL, overwrite=True)
            # Write OPC configuration
            with fsspec.open(Env.OPCUA_FILEURL, "w", encoding = "utf-8") as fid:
                dump =  yaml.dump(opcua_conf, allow_unicode=True, encoding=None)
                fid.write( dump )

        else:
            # Write Forte project remote
            prj_4diac.write_fboot(Env.FBOOT_FILEURL, overwrite=True,
                host=Env.FBOOT_SSH_IP, port=int(Env.FBOOT_SSH_PORT),
                username=Env.FBOOT_SSH_USERNAME)
            # Write OPC configuration remote
            with fsspec.open(Env.OPCUA_FILEURL, "w", encoding = "utf-8", host=Env.FBOOT_SSH_IP, 
                port=int(Env.FBOOT_SSH_PORT), username=Env.FBOOT_SSH_USERNAME) as fid:
                dump =  yaml.dump(opcua_conf, allow_unicode=True, encoding=None)
                fid.write( dump )

        # Return Status
        res = True

    except Exception as exc:
        msg = str(exc).split('\n')[0]
        msg = f'Unexpected Error Found: "{msg}"'
        raise HTTPException(status_code=520, detail=msg)

    return(res)
# --------------------
