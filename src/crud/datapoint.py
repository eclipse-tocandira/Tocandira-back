'''
This module holds the functions to
access the DataPoint Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from .. import models
from ..env import Enviroment as Env
from ..plc_datapoint import schemas


#######################################

class Tdatapoint:
    ''' Class with CRUD methods to access the DataPoint table.\n
    '''
    