""" 
Query

Contains base class for writers with logic for checking against foreign 
    key constraints.

"""

from api.models import *
from sqlalchemy.inspection import inspect
import pandas as pd

import logging

querylogger = logging.getLogger(__name__)


class Query():
    def __init__(self, data, model):
        self.data = data
        self.known_constraints = self.get_known_constraints(model)

    # def check_constraints(self, session, model, record):
    #     for foreign_key in get_known_constraints(model)['foreign_keys']:
    #         key_name = foreign_key.split()[1]
    #         if key_name in data.columns:
    #             querylogger.info(f'{key_name} found in query.  Checking for existing entry.')
    #             exists = check_exists(model=model, id_column=key_name, session=session, record)
    #             if not exists:
    #                 querylogger.info(f'{record[key_name]} did not return existing row.  Generating empty entry.')
    #                 object_to_add = generate_new_object(model=model, record={foreign_key: record[foreign_key]})
    #                 session.add(object_to_add)
    #                 session.commit()
    
    @staticmethod
    def get_known_constraints(model):
        # Get primary keys in model
        primary_keys = [key.name for key in inspect(model).primary_key]
        # Get foreign keys in model
        foreign_key_sets = [column.foreign_keys for column in inspect(model).columns \
                                                    if len(column.foreign_keys) > 0]
        foreign_keys = [list(keys)[0] for keys in foreign_key_sets]  # TODO: build 
        return {
            'primary_keys': primary_keys, 
            'foreign_keys': [key.target_fullname for key in foreign_keys]
        }

    @staticmethod 
    def check_exists(session, model, record, id_column):
        # Make command to evaluate
        eval_string = f"session.query({model}).filter_by({id_column}=record['{id_column}']).scalar()"
        # Evaluate and return result
        return eval(eval_string)


    @staticmethod
    def dataframe_to_dict(data:pd.DataFrame) -> dict:
        return data.to_dict('records')


    @staticmethod 
    def make_or_update(**kwargs):
        #TODO
        NotImplemented
    