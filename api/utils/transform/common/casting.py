from dateutil.parser import parse

def convert_to_datetime(time_string):
    try:
        date_val = parse(time_string)
        if pd.isnull(date_val):
            return None
        return date_val
    except:
        return None