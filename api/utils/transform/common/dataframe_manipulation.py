##############################
### DataFrame Manipulation ###
##############################
import pandas as pd

from .casting import convert_to_datetime
from .model_helpers import get_columns
from functools import partial

import logging

tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


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
    # Force all null values to None rather than mixed type with np.nan, NaT
    def _replace_nat(series:pd.Series)->pd.Series:
        new_series = series.mask(series.isnull(), None)
        return new_series

    def _replace_empty_strings(x):
        if x == '':
            return None 
        return x

    temp_data = data.copy()
    temp_data = temp_data.where(data.notnull(), None)
    for col in temp_data.columns[temp_data.dtypes == object]:
        temp_data[col] = temp_data[col].apply(_replace_empty_strings)
    # Date cleanup
    date_columns = [column for column in temp_data.columns if "date" in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].astype('object')
        tlogg.info(f'Cleaning Null Dates from Column: {col}')
        temp_data[col] = _replace_nat(temp_data[col])
    return temp_data


def drop_unnamed_columns(df:pd.DataFrame)->pd.DataFrame:
    keep_columns = [col for col in df.columns if len(col)>0]
    return df[keep_columns].copy()


def dates_to_string(df:pd.DataFrame)->pd.DataFrame:
    temp_data = df.copy()
    date_columns = [column for column in temp_data.columns if "date" in column]
    
    for column in date_columns:
        temp_data[column] = temp_data[column].astype('object')
    return temp_data


def null_transform(data: pd.DataFrame):
    return data


def make_column_filter(model):
    return partial(filter_columns, model=model)