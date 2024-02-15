'''
This module hold the endpoints for the 
communication test feature\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
* pyfboot
'''

# Import system libs
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import pyfboot.typelibrary as tlib

# Import custom libs
from . import schemas
from ..env import Enviroment as Env
from ..database import get_db
from ..crud.datapoint import Tdatapoint
from ..crud.datasource import Tdatasource
from ..crud.collector import Tcollector
from ..user_auth import routes as usr_routes


#######################################

# HACK: The test function block was only implemented in
#       snap7 format, so this overload is necessary.
class Snap7Siemens(tlib.SiemensFB):
    ''' Oveload of Siemens function block class to force
    the usage of snap7 library on tests.\n
    '''
    def _is_old_plc(self):
        return(False)

# XXX: If the overload above was not needed we could use
#      the pyfboot.gateway.MonoGatewayProject.PROTOCOL_MAPPING
#      instead of re-defining it here.
PROTOCOL_TYPELIBRARY_MAPPING = {
    'Siemens':Snap7Siemens,
    'Modbus':tlib.ModbusFB,
    'Rockwell':tlib.CipFB,
}

# --------------------
def _parse_opc_response(res:list):
    ''' Get the opc method call response and parse it.\n
    `res` (list): The response from OPC call method\n
    return `info` (schemas.comTest): Parsed response.\n
    '''
    info = schemas.comTest(
        status=res[0],
        message=res[1],
        response=res[2]
    )

    return(info)
# --------------------

# --------------------
def _test_server_connect(endpoint:str,function:str,param:str):
    ''' Conect to the OPC-UA Test server and executes a function.\n
    `endpoint` (str): The connection endpoint.\n
    `function` (str): The function name to call in OPC-UA.\n
    `param` (str): The parameter to pass to the function.\n
    return `response` (list): The function results.\n
    '''
    # Initialize response
    response = [False, "Unknown Error", 0]

    # Open the connection with OPC-UA
    try:
        # TODO: Need to use another OPCua client because the python-opcua
        #       has a license issue with Eclipse Lincense.
        pass

        # # Insert parameters
        # from opcua import Client
        # opc_client = Client(endpoint)
        # # Open
        # opc_client.connect()
        # opc_objects = opc_client.get_objects_node()
        # # Call the remote method
        # response = opc_objects.call_method(function, param)
        # # Close
        # opc_client.disconnect()
    
    # Error handling
    except Exception as exc:
        msg = "Test Server - "+str(exc).split('\n')[0]
        response = [False, msg, 0]
    
    return(response)
# --------------------

# --------------------
def test_plc_connection(dp_name:str, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Test the connection of a specific datapoint.\n
    `dp_name` (str): DataPoint name.\n
    return `res` (JSONResponse): A `schemas.comTest` automatically parsed into
    a HTTP_OK response.\n
    '''
    # Get informations on point and source
    dp = Tdatapoint.get_datapoint_by_name(db, dp_name)
    if ( dp==None ):
        raise HTTPException(status_code=404, detail=f"DataPoint '{dp_name}' not found.")
    ds = Tdatasource.get_datasource_by_name(db, dp.datasource_name)
    if ( ds==None ):
        raise HTTPException(status_code=404, detail=f"DataSource '{dp.datasource_name}' not found.")
    
    # Get the protocol function block class
    prot = ds.protocol.name
    fbclass = PROTOCOL_TYPELIBRARY_MAPPING[prot]
    # Get the collector information
    col = Tcollector.get_by_id(db,ds.collector_id)

    # Initialize the FB to parse parameters

    # NOTE: The ds.timeout will not be used because the
    #       opc method timeout is 4s. Therefore this
    #       connection timeout should be smaller.
    fb = fbclass(timeout=1000)
    
    dpd = dp.dict()
    if 'func_code' in dpd['access']['data'].keys():
        dpd['access']['data']['func_code'] = int(dpd['access']['data']['func_code'].split('-')[0])
    fb.parse_params(ds.dict(),dpd)
    # Get the communication string
    comm_str = fb.get_comm_string()
    # Build the method name to CALL
    method_name = '1:Test' + prot + dp.num_type.upper()

    # Call the test server to check
    opc_response = _test_server_connect(f"opc.tcp://{col.ip}:{Env.OPCUA_TESTER_PORT}", method_name, comm_str)
    # Parse the response
    response = _parse_opc_response(opc_response)
    
    return(response)
# --------------------