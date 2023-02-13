'''
This module contais the schemas
expected in HTTP responses.\n\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel
from typing import Any

#######################################

class comTest(BaseModel):
    status: bool
    message: str
    response: Any