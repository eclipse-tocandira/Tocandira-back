'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
'''

# Import system libs
from typing import Dict, List
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

# Import custom libs
from . import AppInfo
from . import database
from .env import Enviroment as Env
from .crud import Tuser
from .database import SessionManager, engine
from .user_auth import schemas as auth_schemas
from .user_auth import routes as auth_routes
from .plc_datasource import schemas as ds_schemas
from .plc_datasource import routes as ds_routes
from .plc_datapoint import schemas as dp_schemas
from .plc_datapoint import routes as dp_routes
from .collector import schemas as col_schemas
from .collector import routes as col_routes
from .fboot_gen import routes as fboot_routes
from .com_test import schemas as com_schemas
from .com_test import routes as com_routes


#######################################

database.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path=f"{Env.API_NAME}", **AppInfo.__dict__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with SessionManager() as db:
    # Check for users and create a default one if empty
    if (len(Tuser.get_all(db))==0):
        admin_usr = auth_schemas.UserCreate(name='admin', password='admin',
            change_password=True, is_admin=True)
        Tuser.create(db,admin_usr)

# Application Routes 

### Authentication
app.add_api_route("/login",
    methods=["POST"], response_model=auth_schemas.LoginSucess,
    endpoint=auth_routes.authentication)
app.add_api_route("/validate",
    methods=["GET"], response_model=bool,
    endpoint=auth_routes.check_token)

### Defaults
app.add_api_route("/protocol_defaults",
    methods=["GET"], response_model=ds_schemas.comboBox,
    endpoint=ds_routes.get_protocol_defaults)

app.add_api_route("/datasource_defaults/{prot_name}",
    methods=["GET"], response_model=ds_schemas.dataSourceInfo,
    endpoint=ds_routes.get_datasource_defaults)

app.add_api_route("/datapoint_defaults/{prot_name}",
    methods=["GET"], response_model=dp_schemas.dataPointInfo,
    endpoint=dp_routes.get_datapoint_defaults)

app.add_api_route("/collector_defaults",
    methods=["GET"], response_model=col_schemas.collectorInfo,
    endpoint=col_routes.get_collector_defaults)

### Collector
app.add_api_route("/collector/{id}",
    methods=["PUT"], response_model=col_schemas.collector,
    endpoint=col_routes.update_collector)

app.add_api_route("/collector/{id}",
    methods=["GET"], response_model=col_schemas.collector,
    endpoint=col_routes.get_collector)

app.add_api_route("/collector/{id}/status",
    methods=["GET"], response_model=col_schemas.collectorStatus,
    endpoint=col_routes.check_collector_status)

app.add_api_route("/collector/{id}/check",
    methods=["GET"], response_model=col_schemas.collector,
    endpoint=col_routes.check_collector_access)

app.add_api_route("/collector/{id}",
    methods=["DELETE"], response_model=Dict[int,bool],
    endpoint=col_routes.del_collector)

app.add_api_route("/collector",
    methods=["POST"], response_model=col_schemas.collector,
    endpoint=col_routes.new_collector)

app.add_api_route("/collectors",
    methods=["GET"], response_model=List[col_schemas.collector],
    endpoint=col_routes.get_all_collectors)

app.add_api_route("/collectors/status",
    methods=["GET"], response_model=List[col_schemas.collectorStatus],
    endpoint=col_routes.check_collectors_status)

app.add_api_route("/check_ssh_access",
    methods=["POST"], response_model=Dict[str,str],
    endpoint=col_routes.check_ssh_access)

### DataSources
app.add_api_route("/datasource",
    methods=["POST"], response_model=ds_schemas.dataSource,
    endpoint=ds_routes.create_datasource)

app.add_api_route("/datasource",
    methods=["PUT"], response_model=ds_schemas.dataSource,
    endpoint=ds_routes.update_datasource)

app.add_api_route("/datasource/{ds_name}",
    methods=["GET"], response_model=ds_schemas.dataSource,
    endpoint=ds_routes.get_datasource_by_name)

app.add_api_route("/datasource/{ds_name}",
    methods=["DELETE"], response_model=Dict[str,bool],
    endpoint=ds_routes.del_datasource_by_name)

app.add_api_route("/datasource/{ds_name}={active}",
    methods=["PUT"], response_model=Dict[str,bool],
    endpoint=ds_routes.change_datasource_active_status)

app.add_api_route("/datasources",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources)

app.add_api_route("/datasources/range/{ini}-{end}",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources_by_range)

app.add_api_route("/datasources/pending",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources_pending)

app.add_api_route("/datasources/active",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources_active)

app.add_api_route("/datasource/{ds_name}/confirm",
    methods=["PUT"], response_model=Dict[str,bool],
    endpoint=ds_routes.confirm_datasources)

### DataPoints
app.add_api_route("/datapoint",
    methods=["POST"], response_model=dp_schemas.dataPoint,
    endpoint=dp_routes.create_datapoint)

app.add_api_route("/datapoint",
    methods=["PUT"], response_model=dp_schemas.dataPoint,
    endpoint=dp_routes.update_datapoint)

app.add_api_route("/datapoint/{dp_name}",
    methods=["GET"], response_model=dp_schemas.dataPoint,
    endpoint=dp_routes.get_datapoint_by_name)

app.add_api_route("/datapoint/{dp_name}",
    methods=["DELETE"], response_model=Dict[str,bool],
    endpoint=dp_routes.del_datapoint_by_name)

app.add_api_route("/datapoint/{dp_name}={active}",
    methods=["PUT"], response_model=Dict[str,bool],
    endpoint=dp_routes.change_datapoint_active_status)

app.add_api_route("/datapoints",
    methods=["GET"], response_model=List[dp_schemas.dataPoint],
    endpoint=dp_routes.get_datapoints)

app.add_api_route("/datapoints/range/{ini}-{end}",
    methods=["GET"], response_model=List[dp_schemas.dataPoint],
    endpoint=dp_routes.get_datapoints_by_range)

app.add_api_route("/datapoints/pending",
    methods=["GET"], response_model=List[dp_schemas.dataPoint],
    endpoint=dp_routes.get_datapoints_pending)

app.add_api_route("/datapoints/active",
    methods=["GET"], response_model=List[dp_schemas.dataPoint],
    endpoint=dp_routes.get_datapoints_active)

app.add_api_route("/datapoint/{dp_name}/confirm",
    methods=["PUT"], response_model=Dict[str,bool],
    endpoint=dp_routes.confirm_datapoints)

### ForteGateway
app.add_api_route("/export/collector/{id}",
    methods=["POST"], response_model=bool,
    endpoint=fboot_routes.export_gateway)

### Communication Tests
app.add_api_route("/test/{dp_name}",
    methods=["POST"], response_model=com_schemas.comTest,
    endpoint=com_routes.test_plc_connection)

### User Management
app.add_api_route("/user",
    methods=["POST"], response_model=auth_schemas.User,
    endpoint=auth_routes.create_user)

app.add_api_route("/user/password",
    methods=["PUT"], response_model=bool,
    endpoint=auth_routes.change_password)

app.add_api_route("/user/{username}",
    methods=["DELETE"], response_model=bool,
    endpoint=auth_routes.delete_user)

app.add_api_route("/users",
    methods=["GET"], response_model=List[auth_schemas.User],
    endpoint=auth_routes.get_user_list)
