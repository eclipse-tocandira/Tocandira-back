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
    port: int
    update_period: int
    timeout: int
