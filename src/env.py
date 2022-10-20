'''
This module holds all enviroment variables
that are used in the application.\n
Copyright (c) 2017 Aimirim STI.\n
'''

# Import system libs
import os

#######################################

class Enviroment:
    ''' This class hold the set of enviroment variables
    that affect this application.\n
    '''
    API_NAME = os.getenv('CONF_API_NAME', default='api')
    '''`API_NAME` (str): The name of the API route as wanted in 
    `/{name}/{version}`. Default is `"api"`'''
    API_VERSION = os.getenv('CONF_API_VERSION', default='v0')
    '''`API_NAME` (str): The version of the API route as wanted in
    `/{name}/{version}`. Default is `"v0"`'''
    DATABASE_URL = os.getenv('CONF_DATABASE_URL', default='sqlite:///db/sql_app.db')
    '''`DATABASE_URL` (str): The SQL URL to find the `sql_app.db` file.
    Default is `"sqlite:///db/sql_app.db"`'''