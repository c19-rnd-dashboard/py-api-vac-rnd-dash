"""
Transforms

Contains custom source transforms
"""

from sqlalchemy import inspect
import pandas as pd
from datetime import datetime
from api.models import *
from dateutil.parser import parse

import logging

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


##############################
### DataFrame Manipulation ###
##############################

def filter_columns(data:pd.DataFrame, model):
    """ Return only columns that match filter from DataFrame """
    valid_columns = set(get_columns(model))
    supplied_columns = set(data.columns) 
    tlogg.info(f'Supplied Columns: {supplied_columns}\nValid Columns: {valid_columns}')
    filter_set = list(valid_columns.intersection(supplied_columns))
    return data[filter_set]

def cast_dates(data:pd.DataFrame):
    """ Check for date columns and cast objects as datetime """
    temp_data = data.copy()
    date_columns = [column for column in temp_data.columns if 'date' in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].apply(convert_to_datetime)
    return temp_data