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
        self.model = model
        self.known_constraints = self.get_known_constraints(model)
    
    def instrospect_model(self):
        constraints = get_known_constraints(self.model)
        self._primary_keys = constraints['primary_keys']
        self._foreign_keys = constraints['foreign_keys']

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
    def validate_constraints(session, model, record, foreign_keys):
        for target_fullname in foreign_keys:
            # Validate Constraints
            key = target_fullname.split('.')[1]
            model_name = target_fullname.split('.')[0]
            key_model = eval(f'{model_name}')
            exists = check_exists(session=session, model=key_model, record=record, id_column=key)
            if not exists:
                querylogger.info(f"{record['key']} did not return existing row.  Generating placeholder object.")
                placeholder_object = eval(f"{model_name}({key}={record[key]})")
                session.add(placeholder_object)
                session.commit()

    @staticmethod
    def dataframe_to_dict(data:pd.DataFrame) -> dict:
        return data.to_dict('records')

    @staticmethod 
    def make_or_update(session, model, record, primary_key, foreign_keys=None):
        # Build Primary Key for Exists
        if type(primary_key) == list:
            first_primary_key = primary_key[0]
        else:
            first_primary_key = primary_key
        exists = check_exists(session=session, model=key_model, record=record, id_column=first_primary_key)
        if not exists:
            querylogger.info(f"{record['key']} did not return existing row.  Generating placeholder object.")
            placeholder_object = generate_object()
            with session.no_autoflush:
                session.add()
        else:
            with session.no_autoflush:
                update_record(model=model, id_column=id_column, session=session, record=record)
    
    @staticmethod
    def update_record(model, id_column, record, session):
        # Make command to evaluate
        eval_string = f"session.query({model})"