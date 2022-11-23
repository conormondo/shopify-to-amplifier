
import json
import pandas as pd

def get_orders(path):
    ''' Loads file of orders, returns DataFrame'''
    return pd.read_csv(path, dtype=str)

def get_column_keys():
    '''
    Returns the traslative dictionary of amplifier -> shopify flat file
        column names.
    '''
    with open('columns.json', 'r') as file:
        data = json.load(file)
    return data


def get_shipping_data(type):
    '''
    Loads shipping.json file and returns type of region
        Ex. international or domestic
        
    ":param type str: which key to return from json shipping data
        'domestic' or 'international'
    '''
    allowed_type = f'{type.lower()}_allowed'
    with open('shipping.json', 'r') as file:
        data = json.load(file)
    return data[allowed_type]


def map_shipping_method(method, country):
    '''
    Loads shipping data and maps the current shopify method to whatever
        the Amplifier counterpart is
    '''
    if country.upper() == 'US':
        region = 'domestic'
    else:
        region = 'international'

    allowed = get_shipping_data(region)
    if method in allowed:
        return allowed[method]
    else:
        return allowed['Default']
