from sqlalchemy import inspect
from api.models import *
from api.db import get_session

def get_columns(model):
    """ Get all column names from SQL Alchemy Model """
    inst = inspect(model)
    column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    return column_names


def get_product_names():
    """ Get all product preferred names currently in raw """
    with get_session() as session:
        prod_names = session.query(ProductRaw.preferred_name).all()
    return [x[0] for x in prod_names]


def get_sponsors():
    """ Get all sponsors currently in DB """
    with get_session() as session:
        sponsors = session.query(Sponsor.sponsor_id, Sponsor.sponsor_name).all()
    return pd.DataFrame(sponsors, columns=['sponsor_id', 'sponsor_name'])


