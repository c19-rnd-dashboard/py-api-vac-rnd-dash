#product_contact.py


import logging
import pandas as pd

from api.utils.transform import rename_columns
from .product_renaming import product_schema


tlog = logging.getLogger(__name__)

def product_contact_transformer(dataframe: pd.DataFrame) -> pd.DataFrame:
    keep = [
        'ID',
        'Source?',
        'Contact Name',
        'Contact Phone Number', 
        'Contact Email', 
        'Contact Website', 
        'Contact Notes',
    ]

    temp_data = dataframe.copy()[keep]
    temp_data = rename_columns(temp_data, product_schema)
    temp_data = temp_data.query("source=='No'")
    return temp_data