##############################
### DataFrame Manipulation ###
##############################
import pandas as pd

from .casting import convert_to_datetime
from .model_helpers import get_columns
from functools import partial

import logging

tlogg = logging.getLogger(__name__)


def filter_columns(data: pd.DataFrame, model, columns: list = None):
    """ Return only columns that match filter from DataFrame """
    if columns is not None:
        return data[columns]
    else:
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
    # Force all null values to None rather than mixed type with np.nan
    def replace_nat(x):
        if pd.isnull(x):
            return None
        return x
    def replace_empty_strings(x):
        if x == '':
            return None 
        return x

    temp_data = data
    temp_data = temp_data.where(data.notnull(), None)
    for col in temp_data.columns[temp_data.dtypes == object]:
        temp_data[col] = temp_data[col].apply(replace_empty_strings)
    # Date cleanup
    date_columns = [column for column in temp_data.columns if "date" in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].apply(replace_nat)
    return temp_data


def drop_unnamed_columns(df:pd.DataFrame)->pd.DataFrame:
    keep_columns = [col for col in df.columns if len(col)>0]
    return df[keep_columns].copy()