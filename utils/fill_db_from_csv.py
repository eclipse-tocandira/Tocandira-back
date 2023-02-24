'''
This program convert a Excel spreadsheet
to an fboot of a OPC-UA Gateway.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pyfboot
* pyyaml
* pandas
'''

# Import system libs
import pandas as pd
import requests

#######################################

# --------------------
def db_set(data:dict, backend_url:str):
    ''' Add the CSV content to the backend DB.\n
    `data` (dict): PLC Data informations.\n
    `backend_url` (str): The backend address.\n
    '''
    
    # Authenticate
    response = requests.post(backend_url+'/login',{'username':'admin','password':'admin'})
    if (response.status_code!=200):
        raise RuntimeError(f'Could not Login.')
    validation = response.json()
    
    headers = {
        "Authorization": validation['token_type']+' '+validation['access_token'],
    }
    # Get DataSources
    for ds in data['DataSources']:
        # A POST request to the API
        dplist = ds.pop('DataPoints', [])

        response = requests.post(backend_url+'/datasource',json=ds,headers=headers)
        if (response.status_code!=200):
            print(response.json())
            raise RuntimeError(f'Could not create DataSource "{ds["name"]}".')

        # Get all DataPoints in this DataSource
        for dp in dplist:
            # A POST request to the API
            response = requests.post(backend_url+'/datapoint',json=dp,headers=headers)
            if (response.status_code!=200):
                raise RuntimeError(f'Could not create DataPoint"{dp["name"]}".')
                
    return()
# --------------------

# --------------------
def translate_datapoint(sr:pd.Series):
    ''' Get a row and parse it into a
    datapoint dictionary.\n
    `sr` (pandas.Series): \n
    return `dp` (dict): DataPoint informations.\n
    '''
    dp = {
        'name': sr['TAG'],
        'description': sr['DESCRIPTION'],
        'num_type': sr['NUM_TYPE'],
        'datasource_name': sr['PLC NAME'],
        'access': {
            'name': 'Siemens',
            'data': {
                'address': sr['ADDRESS']
            }
        }
    }
    return(dp)
# --------------------

# --------------------
def translate_datasource(df:pd.DataFrame):
    ''' Get a datasource group and parse it into
    a dictinary for pyfboot\n
    `df` (pandas.DataFrame): \n
    return `ds` (dict): Datasource informations.\n
    '''
    ds={
        'name':df['PLC NAME'].unique()[0],
        'plc_ip': df['PLC IP'].unique()[0],
        'plc_port': 102,
        'protocol': {
            'name': 'Siemens',
            'data': {
                'plc': df['PLC MODEL'].unique()[0].upper(),
                'rack': 0,
                'slot': 1
            }
        },
        'timeout': 5000,
        'cycletime': 5000,
        'DataPoints':[]
    }

    for i,row in df.iterrows():
        ds['DataPoints'].append(
            translate_datapoint(row)
        )
    
    return(ds)
# --------------------


# Execute
if __name__=='__main__':
    
    # ----------------------------------------
    # Set Input paths
    table_path = './parsed_variables.csv'
    # Set server path
    backend_url = 'http://localhost:8000'
    # ----------------------------------------

    # Load inputs
    df = pd.read_csv(table_path,sep=',',dtype=str)
    # Separate by PLCs
    gplc = df.groupby('PLC NAME',as_index=False)

    # Parse table into dictionary
    plc_data ={'DataSources':[]}     
    for plc in gplc.groups:
        plc_data['DataSources'].append(
            translate_datasource( gplc.get_group(plc) )
        )
    
    # Write the data into the DB
    db_set(plc_data, backend_url)
