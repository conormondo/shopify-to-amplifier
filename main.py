import pandas as pd
import json

# TODO: Make this dyanic. Argparse or file select.
SHOPIFY_ORDERS = './order_export.csv'

def get_orders():
    return pd.read_csv(SHOPIFY_ORDERS, dtype=str)

def get_column_keys():
    with open('columns.json', 'r') as file:
        data = json.load(file)
    return data

def map_shipping_method(method, country):
    # TODO: Pull Shipping methods from settings
    # TODO: Make Default methods in settinds once pulling from there.
    allowed = {
        "Domestic Standard": "Domestic Standard",
        "Vinyl Only Shipping": "Domestic Standard",
        "DHL International Shipping": "International Standard",
        "Free UPS Ground": "Ground",
        "UPS 3-Day": "3 Day",
        "UPS Next Day Air": "Next Day",
        "Domestic Standard Upper Shelf": "Domestic Oversize"
    }
    
    if method in allowed:
        return allowed[method]
    else:
        if country.upper() == 'US':
            return 'Domestic Standard'
        else:
            return 'International Standard'
        
def main():
    
    # Loads data
    new_frame = pd.DataFrame()
    convert_columns = get_column_keys()
    shopify_orders = get_orders()
    
    # First fill in appropriate columns of template. Omits non required
    # TODO: Fix the way the settings outer key works | Kill it. 
    for col in convert_columns['AtoS'].keys():
        shopify_equivalent = convert_columns['AtoS'].get(col, None)
        if shopify_equivalent:
            new_frame[col] = shopify_orders[shopify_equivalent]
        else:
            new_frame[col] = ''
            
    # Cleanup
    # Forward Fill for duplicates per order
    for col in new_frame.columns:
        new_frame[col] = new_frame.groupby('OrderId')[col].ffill()

    # Shipping Method Cleanup
    new_frame['ShippingMethod'] = new_frame.apply(
        lambda o: map_shipping_method(
            o['ShippingMethod'], o['ShippingCountryCode']),
        axis=1
    )

    # Remove pound from order name given in Shopify
    new_frame['OrderId'] = new_frame['OrderId'].str.replace('#', '')
    new_frame.to_csv('upload.csv', index=False)
    return new_frame
    
if __name__ == '__main__':
    main()
