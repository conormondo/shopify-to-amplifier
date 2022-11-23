# Shopify to Amplifier CSV

This is a dumb script to quickly take shopify order exports and reformat them to automatically be imported into my.amplifier.com

## Installation:
The following dependencies are required:
- [Pandas](https://pandas.pydata.org/pandas-docs/stable/)

Or use the requirements.txt file
```
pip install -r requirements.txt
```

## Usage:
Currently the script looks for the default Shopify export format `orders_export.csv`. Soon this will likely be any file with "orders" or "export" or "shopify" in the name with some sort of hierarchy, but not sure where it will land. If you're reading this, then that means it's still on the original file lookup.
### Steps:
1. Clone or download script.
2. Make an `output` directory.
3. Put exported shopify file in project root directory.
4. Run Script.
5. Take upload file that was created and [import](https://my.amplifier.com/orders/import).
## Running the script:
point terminal into this directly and run the following command:
```
python main.py
```
## Updating Amplifier / Shopify Template
If for whatever reason you need to update the template for the Amplifier to Shopify column mappings, just throw the new template file in this directory and run the update: 

```
python update_template.py
```
**NOTE**: that this will create a new mapping in the settings file. Any new columns that are added will be mapped to a `null` in the columns.json file and will need their Shopfiy counterpart manually added instead of the null. Any existing columns on update will keep their shopify mappings, but if a new template no longer has a column in it, that mapping will be lost.

## TODO:
- Logging / overal script communication (number of orders, errors, etc...)
- Do something with orders that cannot be piped into amplifier template for whatever reason?
- Better CLI args for more dynamic file input. Maybe include .bat or .sh to DIY packaging.

## Current Mappings as of 4/20/22 in columns.json