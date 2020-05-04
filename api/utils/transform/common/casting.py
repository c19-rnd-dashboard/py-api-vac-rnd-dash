from dateutil.parser import parse
import pandas as pd
import numpy as np


def convert_to_datetime(time_string):
    try:
        date_val = parse(time_string)
        if pd.isnull(date_val):
            return None
        return date_val
    except:
        return None


def cast_to_int(series: pd.Series)->pd.Series:
    for i, item in enumerate(series):
        try:
            if item is not None and item is not np.nan:
                series.iloc[i] = int(item)
            else:
                series.iloc[i] = np.nan
        except:
            series.iloc[i] = np.nan
    return series.copy()