""" 
Query

Contains base class for writers with logic for checking against foreign 
    key constraints.

"""

from api.models import *
from sqlalchemy.inspection import inspect
import pandas as pd

import logging

querylogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


class Query():
    def __init__(self, data, model):
        self.data = data
        self.model = model
        self.instrospect_model()
    
    def instrospect_model(self):
        querylogger.debug('Running introspection on model.')
        constraints = self.get_known_constraints(self.model)
        self._primary_keys = constraints['primary_keys']
        self._foreign_keys = constraints['foreign_keys']
        querylogger.debug('Collecting model name')
        temp_model = self.model()
        self._model_name = temp_model._class_name

    def make_or_update(self, session, model, record, primary_key, foreign_keys=None):
        # Build Primary Key for Exists
        querylogger.debug('Beginning Make or Update (Upsert)')
        if type(primary_key) == list:
            first_primary_key = primary_key[0]
        else:
            first_primary_key = primary_key

        exists = self.check_exists(
            session=session, 
            record=record, 
            id_column=first_primary_key)

        if exists is None:
            querylogger.debug(f"{record[first_primary_key]} did not return existing row.  Generating placeholder object.")
            new_record = self.generate_object(record=record)
            with session.no_autoflush:
                session.add(new_record)
        else:
            with session.no_autoflush:
                querylogger.debug(f'Updating existing record for {record[first_primary_key]}')
                self.update_record(session=session, record=record, primary_key=first_primary_key)

    def generate_object(self, record:dict):
        assert type(record) == dict
        querylogger.debug(f'Generating object for {self._model_name}')
        return self.model(**record)
    

    def check_exists(self, session, record, id_column):
        # Make command to evaluate
        eval_string = f"session.query({self._model_name}).filter_by({id_column}=record['{id_column}']).scalar()"
        querylogger.debug('Created EVAL string: ' + eval_string)
        # Evaluate and return result
        try:
            exists = eval(eval_string)
            querylogger.debug(f'Exists returned: {exists}')
            return exists
        except Exception as e:
            querylogger.debug(f'Failure: {e}')
            raise

    def update_record(self, record, session, primary_key):
        # Make command to evaluate
        eval_string = f"session.query({self._model_name}).filter({self._model_name}.{primary_key}=='{record[primary_key]}')"
        querylogger.debug('Created EVAL string: ' + eval_string)
        query_result = eval(eval_string)
        querylogger.debug('Updating query result')
        query_result.update(record)

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
    
