import json
import csv
import os

COLUMNS_FILE = 'columns.json'

def get_new_template():
    ''' returns list of header columns '''
    
    files = os.listdir('.')
    for file in files:
        if 'template' in file.lower() and file.endswith('.csv'):
            new_template = file
    try:
        with open(new_template, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
        return header
    except FileNotFoundError:
        print('Unable to open file...')
        
    except UnboundLocalError:
        print('Unable to find template file...')

def get_old_mapping():
    ''' returns dict '''
    with open(COLUMNS_FILE, 'r') as file:
        data = json.load(file)
    return data['AtoS']
        
def main():
    new_template = get_new_template()
    # Exits if no file with 'template' is found.
    if not new_template:
        print('Please make sure this directly has a file with "Template" in the name.')
        return
    
    old_mapping = get_old_mapping()
    new_mapping = dict()
    json_wrap = {'AtoS': None}
    
    # rewrites columns file with new cols, keeps mapped cols from old.
    for col in new_template:
        if old_mapping.get(col, None):
            new_mapping[col] = old_mapping[col]
        else:
            new_mapping[col] = None
        
    json_wrap['AtoS'] = new_mapping
    with open(COLUMNS_FILE, 'w') as outfile:
        json.dump(json_wrap, outfile, indent=3)

if __name__ == '__main__':
    main()