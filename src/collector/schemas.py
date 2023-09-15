'''
This module contaims the schemas
expected in HTTP responses.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel

#######################################

class collectorInfo(BaseModel):
    ip: str
    name: str
    ssh_port: int
    ssh_user: str
    opcua_port: int
    health_port: int
    update_period: int
    timeout: int

class collectorCreate(collectorInfo):
    ssh_pass: str

class collector(collectorInfo):
    id: int
    valid: bool

class connectionStatus(BaseModel):
    ssh: bool
    opcua: bool
    health: bool

class collectorStatus(collector):
    status: connectionStatus