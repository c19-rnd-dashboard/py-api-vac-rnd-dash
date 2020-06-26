import pandas as pd
import numpy as np 

from functools import partial
from fuzzywuzzy import fuzz 

from api.utils.transform.common import *
from api.utils.tools import coalesce

import logging 

tlogg = logging.getLogger(__name__)

####################################
### Trial Source Transformations ###
####################################

def infer_trial_products(data: pd.DataFrame):
    df = data.copy()
    tlogg.info("Inferring product names")
    # Build search string
    df["search_string"] = df["title"] + " " + df["intervention"]
    # Dump product names from database
    product_names = get_product_names(context=False)

    def get_name(val, product_names):
        list_vals = val.split()
        matches = []
        for name in product_names:
            if fuzz.partial_ratio(name, list_vals) > 80:
                matches.append(name)
        data = ",".join(matches)
        if len(data) == 0:
            data = None
        return data

    get_name_fn = partial(get_name, product_names=product_names)
    df["inferred_product"] = df["search_string"].apply(get_name_fn)
    return df


def trial_cleaner(data: pd.DataFrame):
    df = data.copy()
    tlogg.info("Starting trial_cleaner.")

    def clean_lists(x):
        if "," in x:
            temp_list = x.split(",")
        elif ";" in x:
            temp_list = x.split(";")
        else:
            return x

        def clean_list_item(item: str = None):
            assert type(item) == str
            temp_item = item
            temp_item = temp_item.strip()
            temp_item = temp_item.replace('"', "")
            return temp_item

        return ",".join([clean_list_item(item) for item in temp_list])

    def rename_cols(X):
        X = X.rename(
            columns={
                "normed_spon_names": "sponsors",
                "source_register": "registry",
                "date_registration": "registration_date",
                "date_enrollement": "enrollment_date",
                "public_title": "title",
                "results_url_link": "results_link",
                "web_address": "data_source",
                "trialid": "trial_id",
            }
        )
        return X

    # Apply function
    df = rename_cols(df)
    for col in df.columns[df.dtypes == object]:
        df[col] = df[col].apply(clean_lists)

    df["country_codes"] = df["countries"].apply(clean_country)
    # Generate country code lists and clean names
    cdata = df["countries"].apply(clean_country)

    alpha3 = [coalesce(country['alpha3'], '')
                for country in cdata]
    names = [coalesce(country['name'], '')
                for country in cdata]
    df["country_codes"] = alpha3
    df["countries"] = names
    
    tlogg.info(f'Trial Columns: {df.columns}')
    if 'target_enrollment' in df.columns:
        df["target_enrollment"] = cast_to_int(df.target_enrollment)
    return df
