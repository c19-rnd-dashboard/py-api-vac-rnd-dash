"""
Transforms

Contains custom source transforms
"""

from sqlalchemy import inspect
import pandas as pd
from api.models import *

def get_columns(model):
    """ Get all column names from SQL Alchemy Model """
    inst = inspect(model)
    column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    return column_names

def filter_columns(data:pd.DataFrame, model):
    """ Return only columns that match filter from DataFrame """
    valid_columns = set(get_columns(model))
    supplied_columns = set(data.columns) 
    filter_set = list(valid_columns.intersection(supplied_columns))
    return data[filter_set]