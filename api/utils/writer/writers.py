"""
Writers
    Contains table-specific parsers, transformations, and ORM to
    write clean data to DB.

    ** Data MUST be cleaned at Transformation level prior to write or write may fail.
"""

import pandas as pd

from api.models import *
from api.db import get_session
from functools import partial
from .query import Query

import logging

writelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


####################
### Writer Class ###
####################


class Write(Query):
    def __init__(self, data:pd.DataFrame, model, **params):
        super().__init__(data=data, model=model)
        self.execute(**params)

    def execute(self, **params):
        writelogger.info(f'Starting write execution. Processing stack of: {len(self.data)}')
        with get_session() as session:
            for record in self.dataframe_to_dict(self.data):
                self.make_or_update(
                    model=self.model, 
                    record=record,
                    session=session,
                    primary_key=self._primary_keys,
                    )
            session.commit()
            writelogger.info('Stack comitted.')


### Make Function ###

def run_write(data:pd.DataFrame, model, **kwargs):
    Write(
        data = data,
        model = model,
        params = kwargs
    )


### Control Function ###
def write_trial(data: pd.DataFrame):
    """
    Adds a DataFrame of trials to the db as TrialRaw instances.
    """
    writelogger.info('Building TrialRaw writer.')
    run_write(data=data, model=TrialRaw)


def write_product(data: pd.DataFrame):
    """
    Adds a DataFrame of products to the db as ProductRaw instances.
    """
    writelogger.info('Building ProductRaw writer.')
    run_write(data=data, model=ProductRaw)


def write_milestone(data: pd.DataFrame):
    """
    Adds a DataFrame of milestone categories to the db as Milestone instances.
    """
    writelogger.info('Building Milestone writer.')
    run_write(data=data, model=Milestone)


def write_country(data: pd.DataFrame):
    """
    Adds a DataFrame of countries to the db as Country instances.
    """
    writelogger.info('Building Country writer.')
    run_write(data=data, model=Country)


def write_productsponsor(data: pd.DataFrame):
    """
    Adds a DataFrame of product sponsors to the db and ProductSponsor instances.
    """
    writelogger.info('Building ProductSponsor writer.')
    run_write(data=data, model=ProductSponsor)