import pandas as pd
from helpers import get_orders, get_column_keys, map_shipping_method

# TODO: Make this dyanic. Argparse or file select.
SHOPIFY_ORDERS = 'dcon_unfulfilled.csv'

def main():
    
    # Loads data
    new_frame = pd.DataFrame()
    convert_columns = get_column_keys()
    shopify_orders = get_orders(SHOPIFY_ORDERS)
    
    AMPLIFIER_COLUMNS = convert_columns['AtoS'].keys()

    # First fill in appropriate columns of template. Omits non required
    # TODO: Fix the way the settings outer key works | Kill it. 
    for col in AMPLIFIER_COLUMNS:
        shopify_equivalent = convert_columns['AtoS'].get(col, None)
        if shopify_equivalent:
            new_frame[col] = shopify_orders[shopify_equivalent]
        else:
            new_frame[col] = ''
            
    # Cleanup
    # Forward Fill for duplicates per order
    #TODO: Break into df.loc[:,cols] with list of cols to ffill
    if len(new_frame['SKU'].unique()) > 1:
        for col in new_frame.columns:
            new_frame[col] = new_frame.groupby('OrderId')[col].ffill()
        
    errors = new_frame[new_frame['ShippingMethod'].isna()].copy()
    new_frame = new_frame[~new_frame['ShippingMethod'].isna()]

    # Shipping Method
    new_frame['ShippingMethod'] = new_frame.apply(
        lambda o: map_shipping_method(
            o['ShippingMethod'], o['ShippingCountryCode']),
        axis=1
    )

    # Empty billing
    prefix = 'Billing'
    billing_columns = [c for c in AMPLIFIER_COLUMNS if prefix in c]
    for col in billing_columns:
        field = col.split(prefix)[-1]
        shipping_equivalent = f'Shipping{field}'
        new_frame[col] = new_frame[shipping_equivalent]
    
    # Remove pound from order name given in Shopify
    new_frame['OrderId'] = new_frame['OrderId'].str.replace('#', '')
    if not errors.empty:
        print(f'{len(errors)} Orders found with errors.')
        errors.to_csv('output/cannot_upload.csv', index=False)
        
    _fn = '_upload.'.join(SHOPIFY_ORDERS.split('.')) 
    new_frame.to_csv('output/' + _fn, index=False)

    return new_frame
    
if __name__ == '__main__':
    main()
