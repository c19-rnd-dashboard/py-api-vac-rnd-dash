"""
Ingest

Load local and remote data into database. 
"""
import pandas as pd
from time import time
from .loader import load

import logging

ingestlogger = logging.getLogger(__name__)


class Ingest():
    """
    :param category: trial or product source
    :param source: source URI or filepath
    :type category: str; valid=trial, product
    :type source: str or buffer
    """
    def __init__(self, source, category:str = None):
        self.category = category
        self.source = source
        self.start_time = time()
        self.data = load(source)
        self.assign_transformations()

    def assign_transformations(self):
        if self.category == 'trial':
            self._transforms = assign_trial_transforms()
        elif self.category == 'product':
            self._transforms = assign_product_transforms()
        else:
            raise ValueError('Invalid Category Type')

    def transform_data(self):
        self._transformed_data = self.data.copy()
        for transform in self._transforms:
            self._transformed_data = transform(self._transformed_data)


### Control Function ###

def run_ingest(source, category:str):
    ingestlogger.info(f'Starting ingest of source: {source} category: {category}')
    job = Ingest(source=source, category=category)
    try:
        job.transform_data()
        ingestlogger.info(f'Transformation completed at: {time()}')
    except Exception as e:
        ingestlogger.error(f'Transformation failed. \n {e.message} \n {e.args}')



#########################
### Common Transforms ###
#########################

def null_transform(data: pd.DataFrame):
    return data


##################
### Trial Data ###
##################

def assign_trial_transforms(**kwargs):
    """Assemble trial data transforms for clean write"""
    transform_list = [
        null_transform,
        # Add transforms here or 
        # use transform_list.append(new_transform) for dynamic construction
        ]
    return transform_list


####################
### Product Data ###
####################

def assign_product_transforms(**kwargs):
    """Assemble trial data transforms for clean write"""
    transform_list = [
        null_transform,
        # Add transforms here or 
        # use transform_list.append(new_transform) for dynamic construction
        ]
    return transform_list