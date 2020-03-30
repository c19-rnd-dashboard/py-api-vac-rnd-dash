"""
Loaders
    Contains file or IO detection and loading functions for various data streams.
"""

import os
import pandas as pd
import logging

# Logger
loadlogger = logging.getLogger(__name__)


### Base Class ###

class Loader():
    def __init__(self):
        pass
    
    def fetch(self):
        NotImplemented
    
    def transform(self):
        NotImplemented
    
    def fetch_transform(self, **kwargs):
        return self.transform(
                data = self.fetch(**kwargs),
                **kwargs
            )


### Derived Classes ###

class FileLoader(Loader):
    def __init__(self, filename, **kwargs):
        super().__init__()
        self.filename = filename
        self.data_ = None

    def fetch(self, **kwargs):
        # Get filetype to assign loading function
        filetype = infer_filetype(self.filename)
        # Assign loading function
        file_loader = self.assign_file_loader(filetype)
        # Execute loading function
        load_kwargs = self.filter_kwargs(**kwargs)
        return file_loader(self.filename, **kwargs)

    def transform(self, data=None, **kwargs):
        if data is None and self.data_:
            self.transformed_data = self.data_
            return self.data_
        elif data is not None:
            self.transformed_data = data
            return data # Null transform returns data

    def assign_file_loader(self, filetype):
        print(f'<filetype {filetype}>')  # DEBUG
        lookup = {
            'csv': pd.read_csv,
            'xlsx': pd.read_excel,
            'txt': load_text
        }
        return lookup[filetype]

    def filter_kwargs(self, **kwargs):
        # TODO add pertinent filter for Pandas.
        return kwargs


class ObjectLoader(Loader):
    def __init__(self, buffer_var):
        super().__init__()
        self.buffer_var = buffer_var
        self.data_ = None

    def fetch(self, **kwargs):
        print(type(self.buffer_var))
        pass  # No Stream.  Var defined.

    def transform(self, data=None, **kwargs):
        if data is None and self.data_:
            self.transformed_data = self.data_
            return self.data_
        elif data is not None:
            self.transformed_data = data
            return data # Null transform returns data 
        elif data is None:
            return self.buffer_var # Null store return


#########################
### Control Functions ###
#########################

def load(file_or_buffer=None, **kwargs):
    print('file_or_buffer: ', file_or_buffer)  # DEBUG
    if type(file_or_buffer) == str and is_file(file_or_buffer):
        loader = FileLoader(filename=file_or_buffer)
        return loader.fetch_transform()
    else:
        loader = ObjectLoader(buffer_var=file_or_buffer)
        return loader.fetch_transform()


###########################
### Custom File Loaders ###
###########################

def load_text(filepath, **kwargs):
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
        # Test remote URL
        validate_url(file_or_buffer) and infer_filetype(file_or_buffer) is not None
    ]

    logmsg = f"Tests run: {'-'.join([str(x) for x in tests])}"
    loadlogger.info(logmsg)
    # print(logmsg)  # DEBUG

    return True in tests


def validate_url(url):
    from urllib3.util import parse_url
    from urllib3 import PoolManager

    # Parse the URL
    purl = parse_url(url)
    # Use parsed URL as request and test for valid connection
    http = PoolManager()
    r = http.request('GET', purl.url)

    logmsg = f'Checking URL {url}.  Getting status {r.status}'
    loadlogger.info(logmsg)
    # print(logmsg)  # DEBUG

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