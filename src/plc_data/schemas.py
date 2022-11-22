'''
This module contais the schemas
expected in HTTP responses.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel

#######################################

class simpleList(BaseModel):
    defaultValue: str
    menuItems: list

class dataSourceInfo(BaseModel):
    name: str
    plc_ip: str
    plc_port: int
    cycletime: int
    timeout: int
    status: bool
    protocol: dict
