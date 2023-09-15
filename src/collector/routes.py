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
from paramiko import SSHClient, AutoAddPolicy
import socket

# Import custom libs
from . import schemas
from ..database import get_db
from ..crud import Tcollector
from ..user_auth import routes as usr_routes
from ..fboot_gen import routes as fb_routes

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def get_collector_defaults(usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the default values for a collector.\n
    return `info` (JSONResponse): The `schemas.collectorCreate` automatically parsed into
    a HTTP_OK response.\n
    '''
    template = Tcollector.get_defaults()

    return(template)
# --------------------

# --------------------
def get_collector(id:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get the collector entry in database.\n
    `id` (int): The Collector ID.\n
    return `parsed_col` (JSONResponse): The saved `schemas.collector` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_col = Tcollector.get_by_id(db,id)
    
    if (val_col is None):
        m_name = f"Collector data"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")

    parsed_col = Tcollector._parse_collector(val_col)
    return(parsed_col)
# --------------------

# --------------------
def update_collector(id:int,collector:schemas.collectorCreate, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Update the collector entry in the database.\n
    `id` (int): The Collector ID.\n
    `collector` (schemas.collector): The Collector to update.\n
    return `parsed_col` (JSONResponse): Updated data of `schemas.collector` automatically parsed into
    a HTTP_OK response.\n
    '''
    old_col =  Tcollector.get_by_id(db,id)
    parsed_old = Tcollector._parse_collector(old_col)

    val_col = Tcollector.update(db,id,collector)
    parsed_col = Tcollector._parse_collector(val_col)

    if (val_col is None or old_col is None):
        m_name = f"Collector data"
        raise HTTPException(status_code=404, detail=f"Error updating {m_name}.")

    prom_conf = fb_routes._update_prometheus_conf(parsed_old,val_col)
    try:
        fb_routes._write_prometheus_file(val_col,prom_conf)
    except:
        raise HTTPException(status_code=404, detail=f"Error updating Collector from Prometheus file.")

    return(parsed_col)
# --------------------

# --------------------
def new_collector(collector:schemas.collectorCreate, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Creates a new collector in the database.\n
    `collector` (schemas.collectorCreate): New Collector informations.\n
    return `parsed_col` (JSONResponse): Updated data of `schemas.collector` automatically parsed into
    a HTTP_OK response.\n
    '''
    val_col = Tcollector.create(db,collector)

    if (val_col is None):
        m_name = f"Collector data"
        raise HTTPException(status_code=404, detail=f"Error Creating {m_name}.")

    parsed_col = Tcollector._parse_collector(val_col)
    prom_conf = fb_routes._update_prometheus_conf(parsed_col,val_col)
    try:
        fb_routes._write_prometheus_file(val_col,prom_conf)
    except:
        raise HTTPException(status_code=404, detail=f"Error updating Collector from Prometheus file.")

    return(parsed_col)
# --------------------

# --------------------
def get_all_collectors(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get all collector entries in database.\n
    return `parsed_col` (JSONResponse): The saved `schemas.collector` automatically parsed into
    a HTTP_OK response.\n
    '''
    col_list = Tcollector.get_all(db)
    
    if (col_list is None):
        m_name = f"Collectors"
        raise HTTPException(status_code=404, detail=f"Error searching for available {m_name}.")
    
    parsed_list = []
    for c in col_list:
        parsed_list.append(Tcollector._parse_collector(c))
    return(parsed_list)
# --------------------

# --------------------
def check_collector_access(id:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Search for the collector in the database and check it's ssh access.\n
    `id` (int): The Collector ID.\n
    return `parsed_col` (JSONResponse): The saved `schemas.collector` automatically parsed into
    a HTTP_OK response.\n
    '''
    col = Tcollector.get_by_id(db,id)

    if (col is None):
        m_name = f"Collector"
        raise HTTPException(status_code=404, detail=f"Error searching for {m_name}.")

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    
    try:
        ssh.connect(col.ip, username=col.ssh_user, password=col.ssh_pass, port=col.ssh_port, timeout=2)
        col = Tcollector.validate(db,id,valid=True)
    except Exception as ex:
        col = Tcollector.validate(db,id,valid=False)
        print(str(ex))
    
    ssh.close()

    parsed_col = Tcollector._parse_collector(col)
    return(parsed_col)
# --------------------

# --------------------
def _test_ip_port(ip:str,port:int):
    ''' Test the connection to an IP/Port pair.\n
    `ip` (str): The IP address\n
    `port` (port): The port number\n
    return `acessible` (bool): A flag to indicate that the IP/Port pair exist.\n
    '''
    accessible = False
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(0.2)
        test_socket.connect((ip, port))
        test_socket.close()
        accessible = True
    except Exception as ex:
        print(str(ex))
        accessible = False
    
    return(accessible)
# --------------------

# --------------------
def check_collector_status(id:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get overall connection status of the collector.\n
    `id` (int): The Collector ID.\n
    return `status` (JSONResponse): The saved `schemas.collectorStatus` automatically parsed into
    a HTTP_OK response.\n
    '''
    col = Tcollector.get_by_id(db,id)
    if (col is None):
        m_name = f"Collector"
        raise HTTPException(status_code=404, detail=f"Error searching for {m_name}.")

    stat = {
        'ssh': _test_ip_port(col.ip,col.ssh_port),
        'opcua': _test_ip_port(col.ip,col.opcua_port),
        'health': _test_ip_port(col.ip,col.health_port),
    }

    status = schemas.collectorStatus(
        **Tcollector._parse_collector(col).__dict__,
        status=schemas.connectionStatus(**stat)
    )
    return(status)
# --------------------

# --------------------
def check_collectors_status(db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Get overall connection status of the collector.\n
    `id` (int): The Collector ID.\n
    return `status` (JSONResponse): The saved `schemas.collectorStatus` automatically parsed into
    a HTTP_OK response.\n
    '''
    col_list = Tcollector.get_all(db)
    if (col_list is None):
        m_name = f"Collectors"
        raise HTTPException(status_code=404, detail=f"Error searching for {m_name}.")

    status = []
    for col in col_list:
        stat = {
            'ssh': _test_ip_port(col.ip,col.ssh_port),
            'opcua': _test_ip_port(col.ip,col.opcua_port),
            'health': _test_ip_port(col.ip,col.health_port),
        }

        status.append( 
            schemas.collectorStatus(
                **Tcollector._parse_collector(col).__dict__,
                status=schemas.connectionStatus(**stat)
            )
        )
    
    return(status)
# --------------------

# --------------------
def del_collector(id:int, db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Delete the specified entry from database.\n
    `id` (int): The Collector ID.\n
    return `val_dp` (JSONResponse): A `schemas.dataPoint` automatically parsed into
    a HTTP_OK response.\n
    '''
    col = Tcollector.get_by_id(db,id)
    if (col is None):
        m_name = f"Collector"
        raise HTTPException(status_code=404, detail=f"Error on {m_name} deletion.")

    ans = Tcollector.delete_collector(db,id)

    if (ans[id]):
        parsed_col = Tcollector._parse_collector(col)
        prom_conf = fb_routes._delete_prometheus_conf(col)
        try:
            fb_routes._write_prometheus_file(col,prom_conf)
        except:
            raise HTTPException(status_code=404, detail=f"Error removing Collector from Prometheus file.")

    return(ans)
# --------------------