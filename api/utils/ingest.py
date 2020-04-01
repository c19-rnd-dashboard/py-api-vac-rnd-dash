"""
Ingest

Load local and remote data into database.
"""
import pandas as pd
from time import time
from functools import partial

from .loader import load
from .writer import write_trial, write_product
from .transform import filter_columns, cast_dates
from api.models import *

import logging

ingestlogger = logging.getLogger(__name__)


class Ingest():
    """
    :param category: trial or product source
    :param source: source URI or filepath
    :type category: str; valid=trial, product
    :type source: str or buffer
    """

    def __init__(self, source, category: str = None):
        self.category = category
        self.source = source
        self.start_time = time()
        self.data = load(source)
        self.assign_transformations()
        self.assign_writer()

    def assign_transformations(self):
        if self.category == 'trial':
            self._transforms = assign_trial_transforms()
        elif self.category == 'product':
            self._transforms = assign_product_transforms()
        else:
            raise ValueError('Invalid Category Type')

    def assign_writer(self):
        if self.category == 'trial':
            self._writer = write_trial
        elif self.category == 'product':
            self._writer = write_product
        else:
            raise ValueError('Invalid Category Type')

    def transform_data(self):
        self._transformed_data = self.data.copy()
        for transform in self._transforms:
            self._transformed_data = transform(self._transformed_data)

    def write_data(self):
        if self._transformed_data is not None:
            self._writer(self._transformed_data)
        else:
            error_msg = 'Attempting to write Nonetype.  Transform data first.'
            ingestlogger.error(error_msg)
            raise ValueError(error_msg)


### Control Function ###

def run_ingest(source, category: str):
    ingestlogger.info(
        f'Starting ingest of source: {source} category: {category}')

    try:  # will start load automatically
        job = Ingest(source=source, category=category)
        process_time = time() - job.start_time
        ingestlogger.info(f'Load completed in: {process_time}')
    except Exception as e:
        ingestlogger.error(f'Load failed. \n {e}')
        return 'error'  # return statement for unittest
    # Transform Data & Log
    try:
        job.transform_data()
        ingestlogger.info(
            f'Transformation completed in: {(time() - job.start_time) - process_time}')
        process_time = time() - job.start_time
    except Exception as e:
        ingestlogger.error(f'Transformation failed. \n {e}')
        return 'error'  # return statement for unittest
    # Write Data & Log
    try:
        job.write_data()
        ingestlogger.info(
            f'Data write completed in: {(time() - job.start_time) - process_time}')
        process_time = time() - job.start_time
    except Exception as e:
        ingestlogger.error(f'Write failed. \n {e}')
        return 'error'  # return statement for unittest

    ingestlogger.info(f'Ingest completed in {time() - job.start_time}')


#########################
### Common Transforms ###
#########################

def null_transform(data: pd.DataFrame):
    return data


def trial_cleaner(data: pd.DataFrame):
    df = data
    ingestlogger.info('Starting trial_cleaner.')

    def lower(x):
        """
        Lowers capitalization of all observations in a given str type column.
        """
        return x.lower()

    def clean_lists(x):
        if ',' in x:
            temp_list = x.split(',')
        elif ';' in x:
            temp_list = x.split(';')
        else:
            return x

        def clean_list_item(item: str = None):
            assert type(item) == str
            temp_item = item
            temp_item = temp_item.strip()
            temp_item = temp_item.replace('"', '')
            # print(len(temp_item), temp_item)
            return temp_item
        return ','.join([clean_list_item(item) for item in temp_list])

    def rename_cols(X):
        X = X.rename(columns={
            'normed_spon_names': 'sponsors',
            'source_register': 'registry',
            'date_registration': 'registration_date',
            'date_enrollement': 'enrollment_date',
            'public_title': 'title',
            'results_url_link': 'results_link',
            'web_address': 'data_source',
            'trialid': 'trial_id',})
        return X

    # Apply function
    df = rename_cols(df)
    for col in df.columns[df.dtypes == object]:
        df[col] = df[col].apply(lower)
        df[col] = df[col].apply(clean_lists)

    return df


def make_column_filter(model):
    return partial(filter_columns, model=model)


##################
### Trial Data ###
##################


def assign_trial_transforms(**kwargs):
    """Assemble trial data transforms for clean write"""
    transform_list = [
        null_transform,
        trial_cleaner,
        make_column_filter(TrialRaw),
        cast_dates,
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
        make_column_filter(ProductRaw),
        cast_dates,
        # Add transforms here or
        # use transform_list.append(new_transform) for dynamic construction
    ]
    return transform_list
