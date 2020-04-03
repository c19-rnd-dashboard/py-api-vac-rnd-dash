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

writelogger = logging.getLogger(__name__)


####################
### Writer Class ###
####################


class Write(Query):
    def __init__(self, data:pd.DataFrame, model, **params):
        super().__init__(data=data, model=model)
        self.execute(**params)

    def execute(self, **params):
        writelogger.info('Starting write execution')
        with get_session() as session:
            for record in dataframe_to_dict(self.data):
                make_or_update(model=model, record=record))
            writelogger.info('Stack comitted.')
            session.commit()



### Control Function ###
def write_trial(data: pd.DataFrame):
    """
    Adds a DataFrame of trials to the db as TrialRaw instances.
    """
    with get_session() as session:
        for i in range(data.shape[0]):
            curr_data = data.iloc[i].to_dict()
            curr_trial = TrialRaw(**curr_data)
            session.add(curr_trial)
        session.commit()


def write_product(data: pd.DataFrame):
    """
    Adds a DataFrame of products to the db as ProductRaw instances.
    """
    with get_session() as session:
        for i in range(data.shape[0]):
            curr_data = data.iloc[i].to_dict()
            curr_product = ProductRaw(**curr_data)
            session.add(curr_product)
        session.commit()