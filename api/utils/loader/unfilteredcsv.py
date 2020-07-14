
import logging
import csv
import numpy as np
from contextlib import closing
import requests
import codecs

import pandas as pd

loadlogger = logging.getLogger(__name__)



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

    def infer_head_tail(line_counts:np.array, **kwargs)->dict:
        max_val = max(line_counts)
        
        def get_first_max(line_counts:np.array, max_val:int)->int:
            for index, val in enumerate(line_counts):
                if val == max_val:
                    return index
        head = get_first_max(line_counts, max_val)
        
        def get_approximate_tail(line_counts:np.array, sensitivity=3, **kwargs):
            lower_bound_val = min(np.quantile(line_counts, [0.95, 0.75, 0.5, 0.25, 0.125]))
            end_region = []
            for index in range(len(line_counts)-1, -1, -1):
                if line_counts[index] >= lower_bound_val:
                    end_region.append(index)
                    if len(end_region) >= sensitivity:
                        break
            if 'max_len' in kwargs:
                loadlogger.info(f"Max Length given as: {kwargs['max_len']}")
                max_len = kwargs['max_len']
            else:
                max_len = max(end_region)
            return min(max_len, max(end_region)) # Control interp here
                
        tail_region = get_approximate_tail(line_counts, **kwargs)
        
        return {
            'head': head, 
            'tail': tail_region
        }

    def profile_csv(raw_file:np.array, **kwargs)->dict:
        profile = {}
        profile.update(get_line_counts(raw_file))
        profile.update(infer_head_tail(profile['line_counts'], **kwargs))
        return profile

    # Get raw .csv loaded as array
    raw_import = ingest_csv(file_or_url)
    # Profile the .csv file
    profile = profile_csv(raw_import, **kwargs)
    # Build dataframe from inferred attributes
    df = pd.DataFrame(
        raw_import[profile['head']+1:profile['tail']+1],
        columns = raw_import[profile['head']]
        )
    return df