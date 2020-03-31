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
    pass


def write_product(data: pd.DataFrame):
    pass