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
        writelogger.info(f'Starting write execution. Processing stack of: {len(self.data)}')
        with get_session() as session:
            for record in dataframe_to_dict(self.data):
                make_or_update(
                    model=model, 
                    record=record,
                    session=session,
                    )
            session.commit()
            writelogger.info('Stack comitted.')


### Make Function ###

def make_writer(data:pd.DataFrame, model, **kwargs):
    return Write(
        data = data,
        model = model,
        params = kwargs
    )

### Control Function ###
def write_trial(data: pd.DataFrame):
    """
    Adds a DataFrame of trials to the db as TrialRaw instances.
    """
    # try:
    #     writer = make_writer(data=data, model=TrialRaw)
    # except Exception as e:
        
        
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