"""
Ingest

Load local and remote data into database.
"""
import pandas as pd
from time import time
from functools import partial

from .loader import load
from .writer import *
from .transform import *
from api.models import *

from api.utils.registry import Registry

import logging

ingestlogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))
listRegistry = Registry()


class Ingest:
    """
    :param category: trial or product source
    :param source: source URI or filepath
    :type category: str; valid=trial, product
    :type source: str or buffer
    """

    def __init__(self, source, category: str = None, **kwargs):
        self.category = category
        self.source = source
        self.start_time = time()
        self.data = load(source, **kwargs)
        self.assign_transformations(**kwargs)
        self.assign_writer()

    def assign_transformations(self, **kwargs):
        transformer_list = 'assign_' + self.category + '_transforms'
        try:
            assign_list = listRegistry[transformer_list]
            self._transforms = assign_list()
            ingestlogger.info(f'Assigned trasnformer {transformer_list}')
        except Exception as e:
            ingestlogger.error(f'Could not assign transformer. {e}')
            
    def assign_writer(self):
        try:
            self._writer = eval(f"write_{self.category}")
        except Exception as e:
            ingestlogger.error(f'Could not assign writer for \
                {self.category}. {e}')

    def transform_data(self):
        self._transformed_data = self.data.copy()
        for transform in self._transforms:
            self._transformed_data = transform(self._transformed_data)

    def write_data(self):
        if self._transformed_data is not None:
            self._writer(self._transformed_data)
        else:
            error_msg = "Attempting to write Nonetype.  Transform data first."
            ingestlogger.error(error_msg)
            raise ValueError(error_msg)


### Control Function ###


def run_ingest(source, category: str, **kwargs):
    ingestlogger.info(f"Starting ingest of source: {source} category: {category}")

    try:  # will start load automatically
        job = Ingest(source=source, category=category, **kwargs)
        process_time = time() - job.start_time
        ingestlogger.info(f"Load completed in: {process_time}")
    except Exception as e:
        ingestlogger.error(f"Load failed. \n {e}")
        return "error"  # return statement for unittest
    # Transform Data & Log
    try:
        job.transform_data()
        ingestlogger.info(
            f"Transformation completed in: {(time() - job.start_time) - process_time}"
        )
        process_time = time() - job.start_time
    except Exception as e:
        ingestlogger.error(f"Transformation failed. \n {e}")
        return "error"  # return statement for unittest
    # Write Data & Log
    try:
        job.write_data()
        ingestlogger.info(
            f"Data write completed in: {(time() - job.start_time) - process_time}"
        )
        process_time = time() - job.start_time
    except Exception as e:
        ingestlogger.error(f"Write failed. \n {e}")
        return "error"  # return statement for unittest

    ingestlogger.info(f"Ingest completed in {time() - job.start_time}")


#########################
### Common Transforms ###
#########################


def null_transform(data: pd.DataFrame):
    return data


def make_column_filter(model):
    return partial(filter_columns, model=model)


def make_subset_ingest(model, columns:list = None):
    # Run subset ingest and return unaltered data
    def ingest_subset(data: pd.DataFrame, **kwargs):
        run_ingest(
            source=filter_columns(
                data=data, model=kwargs['model'],columns=kwargs['columns']
                ),
            category=kwargs['model'].__tablename__,
        )
        return data
    return partial(ingest_subset, model=model, columns=columns, )


##################
### Trial Data ###
##################


def assign_trial_transforms(**kwargs):
    """Assemble trial data transforms for clean write"""
    transform_list = [
        null_transform,
        trial_cleaner,
        infer_trial_products,
        make_column_filter(TrialRaw),
        cast_dates,
        clean_null,
        # Add transforms here or
        # use transform_list.append(new_transform) for dynamic construction
    ]
    return transform_list
listRegistry.register(assign_trial_transforms)

####################
### Product Data ###
####################


def assign_product_transforms(**kwargs):
    """Assemble trial data transforms for clean write"""
    transform_list = [
        null_transform,
        clean_product_raw,
        make_column_filter(ProductRaw),
        cast_dates,
        clean_null,
        # make_subset_ingest(model=ProductSponsor, columns=['product_id', 'sponsors']),
        # Add transforms here or
        # use transform_list.append(new_transform) for dynamic construction
    ]
    return transform_list
listRegistry.register(assign_product_transforms)

################
### Sponsors ###
################

## Sponsor ##
def assign_sponsor_transforms(**kwargs):
    return [
        clean_null,
    ]
listRegistry.register(assign_sponsor_transforms)

## Product Sponsors ##
def assign_product_sponsor_transforms(**kwargs):
    return [
        make_column_filter(ProductSponsor),
        prep_product_sponsors,
        clean_null,
    ]
listRegistry.register(assign_product_sponsor_transforms)