"""
Loaders
    Contains file or IO detection and loading functions for various data streams.
"""

import os
import pandas as pd
import logging

from urllib3.util import parse_url
from urllib3 import PoolManager

from .unfilteredcsv import load_unfiltered_csv
from .gsheetloader import load_gsheet
from .sourcecache import check_cache, read_cache, cache_source


# Logger
loadlogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


### Base Class ###

class Loader():
    def __init__(self, cache=True):
        self.cache=cache
    
    def fetch(self):
        NotImplemented
    
    def transform(self, data=None, **kwargs):
        if data is None and self.data_:
            self.transformed_data = self.data_
            return self.data_
        elif data is not None:
            self.transformed_data = data
            return data # Null transform returns data
    
    def fetch_transform(self, **kwargs):
        if self.cache:
            if self._check_cache(**kwargs):
                return self._read_cache(**kwargs)

        return self.transform(
                data = self.fetch(**kwargs),
                **kwargs
            )

    def _check_cache(self, *args, **kwargs):
        return check_cache(self, **kwargs)


    def _read_cache(self, *args, **kwargs):
        ## TODO Complete with imported helper function to read data from cache (requires conversion to DataFrame)
        pass






### Derived Classes ###

class FileLoader(Loader):
    def __init__(self, filename, cache=True, **kwargs):
        super().__init__(cache)
        self.filename = filename
        self.data_ = None
        
        self.loader = None
        if 'loader' in kwargs:
            self.loader = kwargs['loader']

    def fetch(self, **kwargs):
        # Get filetype to assign loading function
        filetype = infer_filetype(self.filename)
        # Assign loading function
        file_loader = self.assign_file_loader(filetype, **kwargs)
        # Execute loading function
        return file_loader(self.filename, **kwargs)

    def assign_file_loader(self, filetype, **kwargs):
        print(f'<filetype {filetype}>')  # DEBUG
        lookup = {
            'csv': pd.read_csv,
            'gsheet': load_gsheet,
            'xlsx': pd.read_excel,
            'txt': load_text,
            'unfiltered_csv': load_unfiltered_csv,
        }
        # Look for explicit loader type
        if self.loader is not None:
            return lookup[self.loader]
        return lookup[filetype]


class ObjectLoader(Loader):
    def __init__(self, buffer_var, **kwargs):
        super().__init__()
        self.buffer_var = buffer_var
        self.data_ = None

    def fetch(self, **kwargs):
        print(type(self.buffer_var), self.buffer_var)
        if type(self.buffer_var) == dict or type(self.buffer_var) == tuple:
            loadlogger.info(f"Detected vartype {type(self.buffer_var)}.  Attempting DataFrame casting.")
            return pd.DataFrame(self.buffer_var)
        elif type(self.buffer_var) == pd.DataFrame:
            loadlogger.info(f"Detected pandas DataFrame.  Returning object of shape {self.buffer_var.shape}.")
            return self.buffer_var
        else:
            raise NotImplementedError('Only supporting dict, tuple of arrays, dataframe, objects currently')
        


#########################
### Control Functions ###
#########################

def load(file_or_buffer=None, cache=True, **kwargs):
    # print('file_or_buffer: ', file_or_buffer)  # DEBUG
    if type(file_or_buffer) == str and is_file(file_or_buffer):
        loader = FileLoader(filename=file_or_buffer, cache=cache, **kwargs)
        return loader.fetch_transform(**kwargs)
    else:
        loader = ObjectLoader(buffer_var=file_or_buffer, **kwargs)
        return loader.fetch_transform(**kwargs)


###########################
### Custom File Loaders ###
###########################

def load_text(filepath, **kwargs):
    raise NotImplementedError('Text files to DataFrame incomplete.')
    with open(filepath, 'r') as file:
        data = file.read()
    return data


########################
### Helper Functions ###
########################

valid_filetypes = ['csv', 'json', 'txt', 'xlsx']

def is_file(file_or_buffer):
    # Run a series of tests to decide whether this represents a valid filetype
    tests = [
        # Test for local file
        os.path.isfile(file_or_buffer),
        # Test filepath type requirement
        infer_filetype(file_or_buffer) is not None,
        # Test remote URL
        validate_url(file_or_buffer),
    ]

    logmsg = f"IsFile tests: run: {'-'.join([str(x) for x in tests])}"
    loadlogger.info(logmsg)
    # print(logmsg)  # DEBUG

    return True in tests


def validate_url(url):
    try:
        # Parse the URL
        purl = parse_url(url)
        # Use parsed URL as request and test for valid connection
        http = PoolManager()
        r = http.request('GET', purl.url)

        logmsg = f'Checking URL {url}.  Getting status {r.status}'
        loadlogger.info(logmsg)
        # print(logmsg)  # DEBUG
    except:
        return False

    return r.status == 200


def infer_filetype(filename):
    # Test extension
    extension = filename.split('.')[-1]

    logmsg = f'Checking Extension {extension}.'
    loadlogger.info(logmsg)
    # print(logmsg)  # DEBUG

    if extension in valid_filetypes:
        return extension




if __name__ == "__main__":
    pass