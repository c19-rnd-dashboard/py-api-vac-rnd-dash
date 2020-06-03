import pandas as pd 
import numpy as np 

from api.utils.geolocation import Geolocation

import logging 

tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

#############################
### Product Site Location ###
#############################

def _add_index_as_col(dataframe:pd.DataFrame, col_name) -> pd.DataFrame:
    tlogg.info(f'Adding Column {col_name} to dataframe')
    temp = dataframe.copy()
    temp[col_name] = np.array(temp.index.values)
    return temp

def prep_product_sitelocation(data: pd.DataFrame):
    tlogg.info("Starting prep_product_sitelocations")
    tlogg.info(
        f"Transforming frame of shape {data.shape} and columns {data.columns}")
    ndata = data[data['Source?'] == 'No'].copy()
    ndata = ndata[['ID', 'Sites Locations']]
    return _add_index_as_col(Geolocation.transform(ndata), 'link_id')
