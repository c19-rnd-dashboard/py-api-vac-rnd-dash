"""
Serializers

Series of custom transformations for standard outputs
"""

import json
import logging

from api.utils.registry import Registry

serlogger = logging.getLogger(__name__)
registry = Registry()


class Serializer():
    def __init__(self):
        pass

    def standardize(self, file_or_buffer, **kwargs):
        NotImplemented

    

class DictionarySerializer(Serializer):
    def __init__(self, **kwargs):
        serlogger.info('Creating Dictionary Serializer')
        super().__init__()
        self.assign_transformer(**kwargs)
        
    def standardize(self, file_or_buffer, **kwargs):
        """ Standardize 
            Input to dictionary.  If string, use json loads to bring back to
            python native dictionary. """
        if type(file_or_buffer) == dict:
            return file_or_buffer
        elif type(file_or_buffer) == str:
            try:
                return json.loads(file_or_buffer)
            except Exception as e:
                serlogger.error(f'Could not load string.  Was it valid json? {e}')

    def assign_transformer(self, **kwargs):
        if 'transformer' in kwargs:
            self._transformer = registry[kwargs['transformer']]
        else:
            msg = 'KeyError: transformer not provided.  Cannot assign transformer.'
            serlogger.error(msg)
            raise KeyError(msg)

    def transform(self, file_or_buffer, **kwargs):
        dictionary = self.standardize(file_or_buffer, **kwargs)
        return self._transformer(dictionary)



### Serialization Function ###

def camelcase_keys(dictionary):
    def cap_or_return(x):
        if type(x) == str:
            return x.capitalize()
        else:
            return x
    new_dictionary = {}
    for key in list(dictionary.keys()):
        key_list = key.split('_')
        if len(key_list) > 1:
            key_list = [key_list[0]] + [cap_or_return(x) for x in key_list[1:]]
        new_key = ''.join(key_list)
        new_dictionary[new_key] = dictionary[key]
    return new_dictionary
registry.register(camelcase_keys)