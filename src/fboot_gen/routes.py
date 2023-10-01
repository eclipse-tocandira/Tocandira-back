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
from pydantic.utils import deep_update
import fsspec
import yaml

# Import custom libs
from ..database import get_db
from ..env import Enviroment as Env
from ..user_auth import routes as usr_routes
from ..crud.datapoint import Tdatapoint
from ..crud.datasource import Tdatasource
from ..crud.collector import Tcollector

#######################################

# --------------------
def _update_prometheus_conf(old,db_col):
    ''' Load the existing Prometheus configuration and update it.\n
    `db_col` (schema.collector): The collector information.\n
    return `prometheus_conf` (dict): The `prometheus.yml` file updated for
    this collector.\n
    '''

    prometheus_conf = Env.DEFAULTS['Prometheus']
    
    # Read existing Prometheus File
    try:
        with fsspec.open(Env.PROMETHEUS_FILEURL, 'r', host=db_col.ip, 
            port=int(db_col.ssh_port), username=db_col.ssh_user, password=db_col.ssh_pass) as fid:
            prometheus_conf_r = yaml.safe_load(fid)
        prometheus_conf = deep_update(prometheus_conf,prometheus_conf_r)
    except:
        pass

    # Search for existing configuration
    exporter_id = -1
    for i,conf in enumerate(prometheus_conf['scrape_configs']):
        if(old!=None):
            if( conf['job_name']==old.name ):
                exporter_id = i
    
    # Write data into correct format
    ex_data = { 'job_name': db_col.name,
        'scrape_interval': f"{db_col.update_period}s", 
        'static_configs':[{'labels':{'group':db_col.name},'targets': 
        [f"{db_col.ip}:{db_col.opcua_port}",f"{db_col.ip}:{db_col.health_port}"]}]
    }
    # Insert data in prometheus structure
    if (exporter_id!=-1):
        prometheus_conf['scrape_configs'][exporter_id] = ex_data
    else:
        prometheus_conf['scrape_configs'].append(ex_data)
    
    return(prometheus_conf)
# --------------------

# --------------------
def _delete_prometheus_conf(db_col):
    ''' Load the existing Prometheus configuration and update it.\n
    `db_col` (schema.collector): The collector information.\n
    return `prometheus_conf` (dict): The `prometheus.yml` file updated for
    this collector.\n
    '''

    prometheus_conf = Env.DEFAULTS['Prometheus']

    # Read existing Prometheus File
    try:
        with fsspec.open(Env.PROMETHEUS_FILEURL, 'r', host=db_col.ip, 
            port=int(db_col.ssh_port), username=db_col.ssh_user, password=db_col.ssh_pass) as fid:
            prometheus_conf_r = yaml.safe_load(fid)
        prometheus_conf = deep_update(prometheus_conf,prometheus_conf_r)
    except:
        pass

    # Search for existing configuration
    exporter_id = -1
    for i,conf in enumerate(prometheus_conf['scrape_configs']):
        if( conf['job_name']==db_col.name ):
            exporter_id = i
    
    # Remove data from prometheus structure
    if (exporter_id!=-1):
        _ = prometheus_conf['scrape_configs'].pop(exporter_id)
    
    return(prometheus_conf)
# --------------------

# --------------------
def _write_prometheus_file(db_col, prometheus_conf):
    ''' Description \n
    `` (): \n
    return `` (): \n
    '''
    with fsspec.open(Env.PROMETHEUS_FILEURL, 'w', encoding = "utf-8", host=db_col.ip, 
        port=int(db_col.ssh_port), username=db_col.ssh_user, password=db_col.ssh_pass) as fid:
        p_dump = yaml.dump(prometheus_conf, allow_unicode=True, encoding=None, default_flow_style=False)
        fid.write( p_dump )
# --------------------

# --------------------
def export_gateway(id:int,db:Session=Depends(get_db), usr:str=Depends(usr_routes._check_valid_token)):
    ''' Export active database entries as a Forte OPC-UA gateway fboot file.\n
    return `res` (JSONResponse): A `bool` automatically parser into
    a HTTP_OK response.\n
    '''
    res = False

    val_col = Tcollector.get_by_id(db,id)
    if val_col==None:
        raise HTTPException(status_code=404, detail=f"Error searching for Collector to Export. Invalid ID.")
    
    parsed_col = Tcollector._parse_collector(val_col)

    # Create the 4diac Gateway Project
    prj_4diac = MonoGatewayProject(parsed_col.update_period*1000)

    # Create OPCUA configuration file
    opcua_conf = { 'endPoint':f'opc.tcp://forte_server:4840', 'nodes':[] }

    try:
        # Get active datasources
        ds_list = Tdatasource.get_datasources_active(db)
        for ds in ds_list:
            # Filter datasources for the ones in this collector
            if ds.collector_id!=val_col.id:
                continue
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

        # Get the updated prometheus configuration
        prometheus_conf = _update_prometheus_conf(parsed_col,val_col)
        
        # Write Forte project remote
        prj_4diac.write_fboot(Env.FBOOT_FILEURL, overwrite=True,
            host=val_col.ip, port=int(val_col.ssh_port),
            username=val_col.ssh_user, password=val_col.ssh_pass)
        # Write OPC configuration remote
        with fsspec.open(Env.OPCUA_FILEURL, "w", encoding = "utf-8", host=val_col.ip, 
            port=int(val_col.ssh_port), username=val_col.ssh_user, password=val_col.ssh_pass) as fid:
            dump =  yaml.dump(opcua_conf, allow_unicode=True, encoding=None)
            fid.write( dump )        
        # Write Prometheus File        
        _write_prometheus_file(val_col, prometheus_conf)

        # Return Status
        res = True

    except Exception as exc:
        msg = str(exc).split('\n')[0]
        msg = f'Export Error: "{msg}"'
        raise HTTPException(status_code=520, detail=msg)

    return(res)
# --------------------
