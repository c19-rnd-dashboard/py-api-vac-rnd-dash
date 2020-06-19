import pandas as pd
import numpy as np
import string

from api.utils.transform.common import *

from api.utils.tools import coalesce

from .product_renaming import product_schema
import logging


logger = logging.getLogger(__name__)

######################################
### Product Source Transformations ###
######################################


## DEPRECATED - REMOVE IN FUTURE ITERATION ##
# def renumber_id(data: pd.DataFrame, id_col='ID') -> pd.DataFrame:
#     logger.info(f"Starting id renumber on {id_col}")
#     id_list = []
#     id = 1
#     for i, _ in enumerate(range(len(data))):
#         id_list.append(id)
#         if i%2 != 0:
#             id += 1

#     data['ID'] = id_list
#     return data


def clean_product_raw(data: pd.DataFrame):
    assert type(data) == pd.DataFrame
    assert len(data) > 0
    logger.info("Starting clean_product_raw")
    # Drop columns with no name (assume no data or not relevant)
    temp_data = drop_unnamed_columns(data).copy()
    # Rename columns to db format/names
    temp_data = temp_data.rename(columns=product_schema)

    # Clean Sources and append to data rows
    def get_unique_sources(row_list: list) -> dict:
        url_list = []
        try:
            for item in row_list:
                if ('http' in item):
                    if item not in url_list:
                        url_list.append(item)
            urls = ','.join(url_list)
            product_id = row_list[0]
            return {
                'product_id': product_id,
                'sources': urls,
            }
        except:
            return {'product_id': row_list[0], 'sources':None}

    def clean_valid_sources(df: pd.DataFrame):
        data_rows = df.query("source == 'No'")
        source_rows = df.query("source == 'Yes'")

        clean_sources = []
        for i in range(len(source_rows)):
            row_list = source_rows.iloc[i].to_list()
            clean_sources.append(get_unique_sources(row_list=row_list))

        source_frame = pd.DataFrame(clean_sources)
        clean_frame = data_rows.drop(columns=['source']).merge(
            source_frame, on='product_id')
        return clean_frame

    temp_data = clean_valid_sources(temp_data)
    logger.info('Cleaned asset sources.')
    # Infer preferred_name from other names
    def build_missing_preferred_names(df: pd.DataFrame) -> pd.DataFrame:

        def clean_(item):
            teststr = str(item)
            return teststr.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')

        logger.info('Inferring rule-based preferred names.')
        df1 = df.copy()
        preferred_names = []
        for i in range(len(df)):
            row = df1.iloc[i]
            if len(str(row.preferred_name)) < 2:
                if len(str(row.chemical_name)) > 0:
                    preferred_name = clean_(row.chemical_name)
                elif len(str(row.brand_name)) > 0:
                    preferred_name = clean_(row.brand_name)
                elif (len(str(row.sponsors)) > 0):
                    preferred_name = '-'.join(
                        [
                            clean_(row.sponsors.split(',')[0]),
                            str(row.product_id)
                        ])
                else:
                    preferred_name = None
            else:
                preferred_name = row.preferred_name
            preferred_names.append(preferred_name)

        logger.info('rebuilding preferred name series')
        df1.preferred_name = np.array(preferred_names)
        return df1[df1.preferred_name.str.len() > 0]

    temp_data = build_missing_preferred_names(temp_data)
    logger.info('Preferred names filled where possible.')
    
    # Generate country code lists and clean names
    logger.info("Cleaning Product Countries.")
    cdata = temp_data["countries"].apply(clean_country)

    alpha3 = [coalesce(country['alpha3'], '')
                for country in cdata]
    names = [coalesce(country['name'], '')
                for country in cdata]

    temp_data["country_codes"] = alpha3
    temp_data["countries"] = names

    logger.info("Cleaning lists in object fields.")
    for col in temp_data.columns[temp_data.dtypes == object]:
        temp_data[col] = temp_data[col].apply(clean_lists)

    # Finally, return the prepared dataframe
    return temp_data
