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
    `/{name}/{version}`'''
    API_VERSION = os.getenv('CONF_API_VERSION', default='v0')
    '''`API_NAME` (str): The version of the API route as wanted in
    `/{name}/{version}`'''