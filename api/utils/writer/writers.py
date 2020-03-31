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
            curr_trial = TrialRaw(
                title=data.loc['title', i],
                registry=data.loc['registry', i],
                registration_date=data.loc['registration_date', i],
                enrollment_date=data.loc['enrollment_date', i],
                start_date=data.loc['start_date', i],
                recruitment_status=data.loc['recruitment_status', i],
                intervention_type=data.loc['intervention_type', i],
                sponsors=data.loc['sponsors', i],
                countries=data.loc['countries', i],
                data_reference=data.loc['data_reference', i],
                data_source=data.loc['data_source', i],
                results_link=data.loc['results_link', i]
            )
            session.add(curr_trial)
        session.commit()


def write_product(data: pd.DataFrame):
    """
    Adds a DataFrame of products to the db as ProductRaw instances.
    """
    with get_session() as session:
        for i in range(data.shape[0]):
            curr_product = ProductRaw(
                preferred_name=data.loc['preferred_name', i],
                chemical_name=data.loc['chemical_name', i],
                brand_name=data.loc['brand_name', i],
                repurposed=data.loc['repurposed', i],
                notes=data.loc['notes', i],
                disease=data.loc['disease', i],
                application=data.loc['application', i],
                product_type=data.loc['product_type', i], 
                indication=data.loc['indication', i],
                molecule_type=data.loc['molecule_type', i],
                therapeutic_approach=data.loc['therapeutic_approach', i],
                other_partners=data.loc['other_partners', i],
                num_sites=data.loc['num_sites', i],
                site_locations=data.loc['site_locations', i],
                enrollment_date=data.loc['enrollment_date', i],
                intervention_type=data.loc['intervention_type', i],
                sponsors=data.loc['sponsors', i],
                data_reference=data.loc['data_reference', i],
                data_source=data.loc['data_source', i]
            )
            session.add(curr_product)
        session.commit()