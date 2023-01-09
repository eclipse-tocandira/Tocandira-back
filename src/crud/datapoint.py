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
from ..plc_datasource import schemas as ds_schemas


#######################################

class Tdatapoint:
    ''' Class with CRUD methods to access the DataPoint table.\n
    '''
    
    # --------------------
    @staticmethod
    def get_datapoint_placeholder(prot_name:str):
        ''' Search in DEFAULTS for the placeholders of a specific protocol.\n
        `prot_name` (str): Name of the Protocol to search.\n
        return (schemas.dataPointInfo): The information to pré-fill the fields.\n
        '''
        info = None

        # Check for asked protocol in defaults
        if prot_name in Env.DEFAULTS['Data'].keys():
            this_access = Env.DEFAULTS['Data'][prot_name]

            # Parse protocol specific information
            a_info = {}
            for key, val in this_access['access'].items():
                if('valid' in val.keys()):
                    a_info[key] = ds_schemas.comboBox(defaultValue=val['value'],menuItems=val['valid'])
                else:
                    a_info[key] = val['value']
            
            # Mount Datapoint information structure
            info = schemas.dataPointInfo(
                name=this_access['name']['value'],
                description=this_access['description']['value'],
                num_type=this_access['num_type']['value'],
                ds_name=this_access['ds_name']['value'],
                access=schemas.accessInfo(name=prot_name,data=a_info)
            )

        return(info)
    # --------------------
