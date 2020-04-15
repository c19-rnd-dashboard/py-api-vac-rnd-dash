"""
Loaders
    Contains file or IO detection and loading functions for various data streams.
"""

import os
import pandas as pd
import logging

from urllib3.util import parse_url
from urllib3 import PoolManager

import csv
import numpy as np
from contextlib import closing
import requests
import codecs

# Logger
loadlogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


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
        file_loader = self.assign_file_loader(filetype, **kwargs)
        # Execute loading function
        # load_kwargs = self.filter_kwargs(**kwargs)
        return file_loader(self.filename, **kwargs)

    def transform(self, data=None, **kwargs):
        if data is None and self.data_:
            self.transformed_data = self.data_
            return self.data_
        elif data is not None:
            self.transformed_data = data
            return data # Null transform returns data

    def assign_file_loader(self, filetype, **kwargs):
        print(f'<filetype {filetype}>')  # DEBUG
        lookup = {
            'csv': pd.read_csv,
            'xlsx': pd.read_excel,
            'txt': load_text,
            'unfiltered_csv': load_unfiltered_csv,
        }
        # Look for explicit loader type
        if 'loader' in kwargs:
            return lookup[kwargs['loader']]
        return lookup[filetype]


class ObjectLoader(Loader):
    def __init__(self, buffer_var):
        super().__init__()
        self.buffer_var = buffer_var
        self.data_ = None

    def fetch(self, **kwargs):
        print(type(self.buffer_var), self.buffer_var)
        if type(self.buffer_var) == dict or type(self.buffer_var) == tuple:
            return pd.DataFrame(self.buffer_var)
        elif type(self.buffer_var) == pd.DataFrame:
            return self.buffer_var
        else:
            raise NotImplementedError('Only supporting dict, tuple of arrays, dataframe, objects currently')
        

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
        loader = FileLoader(filename=file_or_buffer, **kwargs)
        return loader.fetch_transform(**kwargs)
    else:
        loader = ObjectLoader(buffer_var=file_or_buffer, **kwargs)
        return loader.fetch_transform(**kwargs)


###########################
### Custom File Loaders ###
###########################

def load_text(filepath, **kwargs):
    with open(filepath, 'r') as file:
        data = file.read()
    return data


def load_unfiltered_csv(file_or_url: str, **kwargs):
    loadlogger.info('<load_unfiltered_csv> Starting .csv data inference')
    def read_to_array(reader)->np.array:
        raw_data = []
        for row in reader:
            raw_data.append(row)
        return np.array(raw_data)

    def ingest_csv(file_or_url)->np.array:
        # Handle HTTP requests
        if 'http' in file_or_url:
            with closing(requests.get(file_or_url, stream=True)) as r:
                reader = csv.reader(
                    codecs.iterdecode(r.iter_lines(), 'utf-8'), 
                    delimiter=',', 
                    quotechar='"',
                )
                return read_to_array(reader)

        # Default handling of .csv file
        with open(file_or_url, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            return read_to_array(reader)

    def get_line_counts(raw_file:np.array)->np.array:
        def count_value(newline:np.array):
            count = 0
            for item in newline:
                if len(item) > 0:
                    count += 1
            return count
        
        return {
            'line_counts': np.array(list(map(count_value, raw_file)))
        }

    def infer_head_tail(line_counts:np.array)->dict:
        max_val = max(line_counts)
        
        def get_first_max(line_counts:np.array, max_val:int)->int:
            for index, val in enumerate(line_counts):
                if val == max_val:
                    return index
        head = get_first_max(line_counts, max_val)
        
        def get_approximate_tail(line_counts:np.array, sensitivity=3):
            lower_bound_val = min(np.quantile(line_counts, [0.95, 0.75, 0.5, 0.25, 0.125]))
            end_region = []
            for index in range(len(line_counts)-1, -1, -1):
                if line_counts[index] >= lower_bound_val:
                    end_region.append(index)
                    if len(end_region) >= sensitivity:
                        break
            return max(end_region) # Control interp here
                
        tail_region = get_approximate_tail(line_counts)
        
        return {
            'head': head, 
            'tail': tail_region,
        }

    def profile_csv(raw_file:np.array)->dict:
        profile = {}
        profile.update(get_line_counts(raw_file))
        profile.update(infer_head_tail(profile['line_counts']))
        return profile

    # Get raw .csv loaded as array
    raw_import = ingest_csv(file_or_url)
    # Profile the .csv file
    profile = profile_csv(raw_import)
    # Build dataframe from inferred attributes
    df = pd.DataFrame(
        raw_import[profile['head']+1:profile['tail']+1],
        columns = raw_import[profile['head']]
        )
    return df


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