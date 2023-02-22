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

    CYCLETIME = os.getenv('CONF_CYCLETIME', default='5000')
    '''`CYCLETIME` (int): Gateway Read execution time'''

    OPCUA_FILEURL = os.getenv('OPCUA_FILEURL', default='./opcua_exporter.yml')
    '''`OPCUA_FILEURL` (str): Local or Remote path to save the generated
    OPCUA Exporter configuration file. Default is `"./opcua_exporter.yml"`'''
    
    OPCUA_TESTER_ENDPOINT = os.getenv('OPCUA_TESTER_ENDPOINT', default='opc.tcp://localhost:4900')
    '''`OPCUA_TESTER_ENDPOINT` (str): The endpoint address to connect the
    test request to. Default is `"opc.tcp://localhost:4900"`'''

    FBOOT_FILEURL = os.getenv('FBOOT_FILEURL', default='./forte.fboot')
    '''`FBOOT_FILEURL` (str): Local or Remote path to save the generated
    Forte fboot file. Default is `"./forte.fboot"`'''
    
    FBOOT_SSH_IP = os.getenv('FBOOT_SSH_IP', default='localhost')
    '''`FBOOT_SSH_IP` (str): IP address to perform ssh connection if needed.
    Default is `"localhost"`'''

    FBOOT_SSH_PORT = os.getenv('FBOOT_SSH_PORT', default='22')
    '''`FBOOT_SSH_PORT` (int): Port number for SSH connection.
    Default is `22`'''

    FBOOT_SSH_USERNAME = os.getenv('FBOOT_SSH_USERNAME', default=None)
    '''`FBOOT_SSH_USERNAME` (str): Username for SSH connection.'''