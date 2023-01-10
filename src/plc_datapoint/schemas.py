'''
This module contais the schemas
expected in HTTP responses.\n\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel

# Import custom libs
from ..plc_datasource import schemas as ds_schemas

#######################################

class accessInfo(BaseModel):
    name: str
    data: dict

class dataPointInfo(BaseModel):
    name: str
    description: str
    num_type: str
    datasource_name: str
    access: accessInfo

class dataPoint(dataPointInfo):
    active: bool
    pending: bool
    # datasource: ds_schemas.dataSource
