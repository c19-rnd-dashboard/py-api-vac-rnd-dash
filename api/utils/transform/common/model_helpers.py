import pandas as pd
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


def get_product_sponsors():
    with get_session() as session:
        sponsors_info = session.query(ProductSponsor.product_id, Sponsor.sponsor_id, Sponsor.sponsor_name).join(ProductSponsor).all()
    return sponsors_info


def get_product_milestones():
    """ Get all product_milestones currently in DB"""
    with get_session() as session:
        milesone_info = session.query(
            ProductMilestone.link_id,
            ProductMilestone.product_id, ProductMilestone.milestone_id, ProductMilestone.date, ProductMilestone.status,
            Milestone.name, Milestone.category).join(ProductMilestone).all()
    return pd.DataFrame(milesone_info, columns=['link_id', 'product_id', 'milestone_id', 'date', 'status', 'milestone_name', 'category'])