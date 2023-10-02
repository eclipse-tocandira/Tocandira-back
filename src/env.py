'''
This module holds all enviroment variables
that are used in the application.\n
Copyright (c) 2017 Aimirim STI.\n
'''

# Import system libs
import os
import json

#######################################

class Enviroment:
    ''' This class hold the set of enviroment variables
    that affect this application.\n
    '''
    SECRET_KEY = os.getenv('CONF_SECRET_KEY', default="9728256cbc2ecc81e478811a29aa5d0d8ae272b8deaec3c552cbb84b55a74908")
    '''`SECRET_KEY` (str): The secret key used in hash algorithm seed.'''

    ALGORITHM = os.getenv('CONF_ALGORITHM', default="HS256")
    '''`ALGORITHM` (str): The encription algorithm used for passwords.'''

    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('CONF_ACCESS_TOKEN_EXPIRE_MINUTES', default="30")
    '''`ACCESS_TOKEN_EXPIRE_MINUTES` (int): Number of minutes to expire user access token.'''

    API_NAME = os.getenv('CONF_API_NAME', default='')
    '''`API_NAME` (str): The name of the API route formated as 
    `/{name}/{version}`. Default is blank `""`.'''
    
    DATABASE_URL = os.getenv('CONF_DATABASE_URL', default='sqlite:///db/sql_app.db')
    '''`DATABASE_URL` (str): The SQL URL to find the `sql_app.db` file.
    Default is `"sqlite:///db/sql_app.db"`'''

    DEFAULT_FILE = os.getenv('CONF_DEFAULT_FILE' ,default='config/defaults.json')
    '''`DEFAULT_FILE` (str): Path to a json file with placeholders for FrontEnd. 
    Default is `"../config/defaults.json"`'''

    DEFAULTS = json.load(open(DEFAULT_FILE,'r'))
    '''`DEFAULTS` (json): Loaded Defaults from DEFAULT_FILE'''

    PROMETHEUS_FILEURL = os.getenv('PROMETHEUS_FILEURL', default='./prometheus.yml')
    '''`PROMETHEUS_FILEURL` (str): Local or Remote path to save the modified
    configuration file for prometheus. Default is `"./prometheus.yml"`'''

    OPCUA_TESTER_PORT = os.getenv('OPCUA_TESTER_PORT', default='4900')
    '''`OPCUA_TESTER_PORT` (str): The OpcUA tester port on forte project. Default is `"4900"`'''