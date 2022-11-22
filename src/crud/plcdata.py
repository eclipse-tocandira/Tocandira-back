'''
This module holds the functions to
access the PlcData Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from ..env import Enviroment as Env
from ..plc_data import schemas


#######################################

class Tplcdata:
    ''' Class with CRUD methods to access the PlcData table.\n
    '''
    
    # --------------------
    @staticmethod
    def get_avail_protocols():
        ''' Search in DEFAULTS for the listed Protocols.\n
        return (schemas.simpleList): All protocols.\n
        '''
        prot_avail = schemas.simpleList(defaultValue='',menuItems=list(Env.DEFAULTS['Protocol'].keys()))

        return(prot_avail)
    # --------------------

    # --------------------
    @staticmethod
    def get_datasource_placeholder(prot_name:str):
        ''' Search in DEFAULTS for the placeholders of a specific protocol.\n
        `prot_name` (str): Name of the Protocol to search.\n
        return (schemas.dataSourceInfo): The information to pré-fill the fields.\n
        '''
        info = None

        # Check for asked protocol in defaults
        if prot_name in Env.DEFAULTS['Protocol'].keys():
            this_prot = Env.DEFAULTS['Protocol'][prot_name]

            # Parse protocol specific information
            p_info = {}
            for key, val in this_prot['protocol'].items():
                if('valid' in val.keys()):
                    p_info[key] = schemas.simpleList(defaultValue=val['value'],menuItems=val['valid'])
                else:
                    p_info[key] = val['value']
            
            # Mount Datasource infromation structure
            info = schemas.dataSourceInfo( name=this_prot['name']['value'],
                plc_ip=this_prot['plc_ip']['value'], plc_port=int(this_prot['plc_port']['value']),
                cycletime=int(Env.CYCLETIME), timeout=int(this_prot['timeout']['value']),
                status=False, protocol=p_info
            )

        return(info)
    # --------------------