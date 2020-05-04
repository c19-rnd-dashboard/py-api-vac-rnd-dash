import logging
import pycountry

tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

def clean_country(country_names: str) -> str:
    result = []
    for country in country_names.split(","):
        try:
            curr_country = pycountry.countries.search_fuzzy(country)
            result.append(curr_country[0].alpha_3)
        except LookupError:
            pass
        except Exception as e:
            tlogg.error(f"Error in country standardization {e}")
    if len(result) == 0:
        return None
    return ",".join(result)


def clean_lists(x):
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