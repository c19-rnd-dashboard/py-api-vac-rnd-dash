"""
Transforms

Contains custom source transforms
"""

from sqlalchemy import inspect
import pandas as pd
from datetime import datetime
from api.models import *


########################
### Helper Functions ###
########################

def get_columns(model):
    """ Get all column names from SQL Alchemy Model """
    inst = inspect(model)
    column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    return column_names


def convert_to_datetime(time_string):
    query_logger.debug('Converting {} to datetime'.format(time_string))
    try:
        assert type(time_string) == str
        return datetime.fromisoformat(time_string)
    except ValueError:
        query_logger.debug('Value Error: Invalid isoformat string')
        query_logger.debug('Sending default datetime')
        return datetime.fromisoformat('1969-01-01')
    except AssertionError as e:
        query_logger.debug('AssertionError: DateTime not a string.')
        raise e
        # query_logger.debug('Attempting translation')
        # return datetime.fromtimestamp(time_string / 1e3)
    except:
        raise


##############################
### DataFrame Manipulation ###
##############################

def filter_columns(data:pd.DataFrame, model):
    """ Return only columns that match filter from DataFrame """
    valid_columns = set(get_columns(model))
    supplied_columns = set(data.columns) 
    filter_set = list(valid_columns.intersection(supplied_columns))
    return data[filter_set]

def cast_dates(data:pd.DataFrame):
    """ Check for date columns and cast objects as datetime """
    temp_data = data.copy()
    date_columns = [column for column in temp_data.columns if 'date' in column]
    for col in date_columns:
        # try:
        pd.to_datetime(temp_data[col])
        # except:
        #     temp_data[col].apply(convert_to_datetime)
        # except:
        #     raise
    return temp_data