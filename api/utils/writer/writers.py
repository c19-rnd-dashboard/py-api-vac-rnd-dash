"""
Writers
    Contains table-specific parsers, transformations, and ORM to
    write clean data to DB.

    ** Data MUST be cleaned at Transformation level prior to write or write may fail.
"""

import pandas as pd

from api.models import *
from api.db import get_session
from api.utils.transform import make_column_filter
from functools import partial
from .query import Query



import logging

writelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


####################
### Writer Class ###
####################


class Write(Query):
    def __init__(self, data: pd.DataFrame, model, **params):
        super().__init__(data=data, model=model)
        self.execute(**params)

    def execute(self, **params):
        writelogger.info(
            f'Starting write execution. Processing stack of: {len(self.data)}')
        with get_session(context=False) as session:
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

def run_write(data: pd.DataFrame, model, **kwargs):
    Write(
        data=data,
        model=model,
        params=kwargs
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


def write_sponsor(data: pd.DataFrame):
    """
    Adds a DataFrame of sponsors to the db as Sponsor instances
    """
    writelogger.info('Building Sponsor writer.')
    run_write(data=data, model=Sponsor)


def write_productsponsor(data: pd.DataFrame):
    """
    Adds a DataFrame of product sponsors to the db and ProductSponsor instances.
    """
    writelogger.info('Building ProductSponsor writer.')
    run_write(data=data, model=ProductSponsor)


def write_productmilestone(data: pd.DataFrame):
    """
    Adds a DataFrame of product milestones to the db and ProductMilestone instances.
    """
    writelogger.info('Building ProductMilestone writer.')
    run_write(data=data, model=ProductMilestone)


def write_sitelocation(data: pd.DataFrame):
    writelogger.info('Building SiteLocation writer.')
    sitelocation_filter = make_column_filter(model=SiteLocation)
    productsitelocation_filter = make_column_filter(model=ProductSiteLocation)
    run_write(data=sitelocation_filter(data), model=SiteLocation)
    run_write(data=productsitelocation_filter(data), model=ProductSiteLocation)
