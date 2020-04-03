"""
Transforms

Contains custom source transforms
"""

from sqlalchemy import inspect
import pandas as pd
import numpy as np
from datetime import datetime
from api.models import *
from api.db import get_session
from dateutil.parser import parse
from fuzzywuzzy import fuzz
from functools import partial
import logging
import pycountry

tlogg = logging.getLogger(__name__)

########################
### Helper Functions ###
########################


def get_columns(model):
    """ Get all column names from SQL Alchemy Model """
    inst = inspect(model)
    column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    return column_names


def convert_to_datetime(time_string):
    try:
        return parse(time_string)
    except:
        return None


def get_product_names():
    """ Get all product preferred names currently in raw """
    with get_session() as session:
        prod_names = session.query(ProductRaw.preferred_name).all()
    return [x[0] for x in prod_names]


##############################
### DataFrame Manipulation ###
##############################


def filter_columns(data: pd.DataFrame, model):
    """ Return only columns that match filter from DataFrame """
    valid_columns = set(get_columns(model))
    supplied_columns = set(data.columns)
    tlogg.info(f"Supplied Columns: {supplied_columns}\nValid Columns: {valid_columns}")
    filter_set = list(valid_columns.intersection(supplied_columns))
    return data[filter_set]


def cast_dates(data: pd.DataFrame):
    """ Check for date columns and cast objects as datetime """
    tlogg.info("Starting date casting")
    temp_data = data.copy()
    date_columns = [column for column in temp_data.columns if "date" in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].apply(convert_to_datetime)
    return temp_data


def clean_null(data: pd.DataFrame):
    # Force all null values to None rathre than mixed type with np.nan
    return data.where(data.notnull(), None)

def clean_country(country_names:list) -> str:
    result = []
    for country in country_names.split(','):
        try: 
            curr_country = pycountry.countries.search_fuzzy(country)
            result.append(curr_country[0].alpha_3)
        except LookupError:
            pass 
        except Exception as e:
            tlogg.error(f'Error in country standardization {e}')
    if len(result) == 0:
        return None
    return ",".join(result)


######################################
### Product Source Transformations ###
######################################


def clean_product_raw(data: pd.DataFrame):
    name_check = data.preferred_name
    # Teste Names
    def test_for_good_name(x):
        return (x is not None) and (len(x) > 2) and (x != np.nan)

    name_check = [test_for_good_name(name) for name in name_check]
    # Build Drop Index for row removal
    drop_ind = [index for index, val in enumerate(name_check) if not val]
    temp_data = data.drop(index=drop_ind)

    def lower(x):
        """
        Lowers capitalization of all observations in a given str type column.
        """
        try:
            return x.lower()
        except:
            return x

    # Apply functions
    for col in temp_data.columns:
        temp_data[col] = temp_data[col].apply(lower)

    return temp_data


def infer_trial_products(data: pd.DataFrame):
    df = data.copy()
    tlogg.info("Inferring product names")
    # Build search string
    df["search_string"] = df["title"] + " " + df["intervention"]
    # Dump product names from database
    product_names = get_product_names()

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
    df = data
    tlogg.info("Starting trial_cleaner.")

    def lower(x):
        """
        Lowers capitalization of all observations in a given str type column.
        """
        return x.lower()

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
        df[col] = df[col].apply(lower)
        df[col] = df[col].apply(clean_lists)
        
    df['countries'] = df['countries'].apply(clean_country)

    return df
