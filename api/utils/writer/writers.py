"""
Writers
    Contains table-specific parsers, transformations, and ORM to
    write clean data to DB.

    ** Data MUST be cleaned at Transformation level prior to write or write may fail.
"""

import pandas as pd

from api.models import *
from api.db import get_session


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