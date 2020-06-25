from dateutil.parser import parse
import pandas as pd
import numpy as np




def _validate_date(d):
    def _is_valid_day(day):
        return (0 < int(day)) and (int(day) < 365)
    def _is_valid_month(month):
        return (0 < int(month)) and (int(month) < 12)
    def _is_valid_year(year):
        return (2017 < int(year)) and (int(year) < 2030)

    def _check_date(d):
        return _is_valid_day(d.day) and _is_valid_month(d.month) and _is_valid_year(d.year)

    if d is not None:
        if _check_date(d):
            return d
    return None



def convert_to_datetime(time_string):
    try:
        date_val = _validate_date(parse(time_string))
        if pd.isnull(date_val):
            return None
        return date_val
    except:
        return None



def cast_to_int(series: pd.Series, replace=True)->pd.Series:
    for i, item in enumerate(series):
        try:
            if item is not None and item is not np.nan:
                series.iloc[i] = int(item)
            else:
                series.iloc[i] = np.nan
        except:
            series.iloc[i] = np.nan
    return series.copy()