"""
Milestone Cleaning, Transformations
"""

import logging 

logger = logging.getLogger(__name__)

## NOTE: Parent table Milestone is fed by reference dataset in data/.  This is only for ProductMilestones or TrialMilestones

import pandas as pd
import numpy as np

from data import factory_milestones, get_milestone_renaming_schema
from api.utils.transform.common import convert_to_datetime


# pd.options.mode.chained_assignment = 'raise'

# Define data preparation and filtering
def fill_product_id(dataframe: pd.DataFrame):
    if 'product_id' in dataframe.columns: 
        pass
    else: 
        try:
            dataframe['product_id'] = dataframe['ID'].astype('int')
        except Exception as e:
            logger.error(f'Could not cast ID. {e}') 
            raise(e)
    return dataframe

    
def remove_value(dictionary:dict, values:list):
    assert type(values) == list, 'Send values as list object'
    temp_list = list(dictionary.values())
    for value in values: temp_list.remove(value)
    return temp_list


def infer_status(value):
    if (value is None) or (value == np.nan):
        return np.nan
    elif convert_to_datetime(value) is not None: 
        return 'COMPLETED'
    elif str(value).strip() == 'SKIPPED':
        return 'SKIPPED'
    elif str(value).split(':')[0] == 'Target':
        return 'ESTIMATED'


def compare_max_completed(row, lookup):
    if row.milestone_id < lookup[row.product_id]:
        return 'COMPLETED'
    return None


def set_max_completed_to_ongoing(row, lookup):
    if row.milestone_id == lookup[row.product_id]:
        return 'ONGOING'
    return row.status
    
def clean_rename_data(dataframe: pd.DataFrame, renaming_schema:dict):
    temp = dataframe.rename(columns=renaming_schema)
    logger.info(f'milestone clean/rename {temp.columns}')
    temp = temp.query("source == 'No'").copy()
    temp = fill_product_id(temp)
    return temp[renaming_schema.values()]


def melt_join_milestones(dataframe: pd.DataFrame, id_vars:list, value_vars:list):
    pivot_data = pd.melt(dataframe, id_vars=id_vars, value_vars=value_vars)
    pivot_data.columns=['product_id', 'name', 'date']
    return pivot_data.merge(
        pd.DataFrame(factory_milestones), 
        how='left', 
        left_on='name', 
        right_on='name')


def build_status(dataframe: pd.DataFrame):
    def get_max_completed(dataframe: pd.DataFrame):
        dataframe['id_completed'] = dataframe.milestone_id * \
                                        (dataframe.status=='COMPLETED')
        return dataframe[['product_id', 'id_completed']]\
                    .groupby(by='product_id')\
                    .max().to_dict()['id_completed']
    
    def fill_completed(dataframe: pd.DataFrame, max_completed: dict):
        fill_status = []
        for i in range(len(dataframe)):
            if dataframe.iloc[i].status is None:
                fill_status.append(
                    compare_max_completed(row=dataframe.iloc[i], lookup=max_completed)
                )
            else:
                fill_status.append(
                    set_max_completed_to_ongoing(row=dataframe.iloc[i], lookup=max_completed)
                )
        dataframe['status'] = fill_status
        return dataframe        
        
    dataframe['status'] = dataframe.date.apply(infer_status)
    fill_completed(dataframe, get_max_completed(dataframe))
    return dataframe
    
def build_link_id(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['link_id'] = dataframe.index.tolist()
    return dataframe

def drop_unavailable_milestones(dataframe: pd.DataFrame) -> pd.DataFrame:
    temp = dataframe[dataframe.status.notna()]
    return temp


def clean_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Re-Cast product_id to integer type
    tempframe = dataframe.copy()
    tempframe.loc[:, 'product_id'] = tempframe.loc[:, 'product_id'].astype('int')
    tempframe = tempframe.drop_duplicates(subset=['product_id', 'milestone_id'], keep='first').copy()
    return tempframe


def milestone_transformer(dataframe: pd.DataFrame) -> pd.DataFrame:
    clean_data = clean_rename_data(dataframe, get_milestone_renaming_schema())
    formatted_data = melt_join_milestones(
        dataframe=clean_data, 
        id_vars=['product_id'], 
        value_vars=remove_value(get_milestone_renaming_schema(), ['product_id', 'source'])
    )
    build_status(formatted_data)
    build_link_id(formatted_data)
    return clean_frame(
        drop_unavailable_milestones(formatted_data)
        )
