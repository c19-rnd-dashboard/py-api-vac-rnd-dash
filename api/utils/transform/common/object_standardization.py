import logging
import pycountry

tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

def clean_country(country_names: str) -> str:
    result = []
    for country in country_names.split(","):
        print('looking up country', country.strip())
        try:
            if country is None or len(country) < 2:
                pass
            else:
                curr_country = pycountry.countries.search_fuzzy(country.strip())
                result.append(curr_country[0].alpha_3)
        except LookupError:
            pass
        except Exception as e:
            tlogg.error(f"Error in country standardization {e}")
    if len(result) == 0:
        return None
    return ",".join(result)


def clean_lists(x:str) -> str:
    if x is None:
        return None 

    if "," in x:
        temp_list = x.split(",")
    elif ";" in x:
        temp_list = x.split(";")
    else:
        return x

    def clean_list_item(item: str = None):
        assert type(item) == str
        temp_item = item
        temp_item = temp_item.strip()
        temp_item = temp_item.replace('"', "")
        return temp_item

    return ",".join([clean_list_item(item) for item in temp_list])


def lower(x):
    """
    Lowers capitalization of all observations in a given str type column.
    """
    try:
        return x.lower()
    except:
        return x