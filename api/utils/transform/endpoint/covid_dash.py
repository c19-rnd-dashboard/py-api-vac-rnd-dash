import pandas as pd



def _clean_date(date):
    if pd.isnull(date):
        return None
    return date


def fetch_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return []


def _seed_dictionary(seed_list, fill_value=[]):
    temp_dict = {}
    [temp_dict.update({seed:fill_value}) for seed in seed_list]
    return temp_dict


def condense_milestones(milestone_results: pd.DataFrame) -> dict:
    unique_ids = milestone_results.product_id.unique()
    milestone_dict = _seed_dictionary(unique_ids)
    for i in range(len(milestone_results)):
        result = milestone_results.iloc[i]
        milestone_info = {
            'milestoneId': int(result.milestone_id),
            'name': result.milestone_name,
            'category': result.category,
            'date': _clean_date(result.date),
            'status': result.status,
        }
        milestone_dict[result.product_id] = milestone_dict[result.product_id] + [milestone_info]
    return milestone_dict


def condense_sponsors(sponsor_results):
    # Requires sponsors in the form (product_id, sponsor_id, sponsor_name)
    print(f'incoming type: {type(sponsor_results)}')
    unique_ids = sorted(list(set([result[0] for result in sponsor_results])))
    sponsor_dict = _seed_dictionary(unique_ids)
    for result in sponsor_results:
        prod_id = result[0]
        spon_id = result[1]
        spon_name = result[2]
        sponsor_info = {'sponsorId': spon_id, 'sponsorName': spon_name}
        sponsor_dict[prod_id] = sponsor_dict[prod_id] + [sponsor_info]
    return sponsor_dict


def condense_locations(location_results: pd.DataFrame) -> dict:
    unique_ids = location_results.product_id.unique()
    location_dict = _seed_dictionary(unique_ids)
    for i in range(len(location_results)):
        result = location_results.iloc[i]
        location_info = {
            'locationId': result.site_location_id,
            'name': result.location_name,
            'city': result.city,
            'state': result.state,
            'country': result.country,
            'lat': result.lat,
            'lng': result.lng
        }
        location_dict[result.product_id] = location_dict[result.product_id] + [location_info]
    return location_dict


def condense_contacts(contact_results: pd.DataFrame) -> dict:
    unique_ids = contact_results.product_id.unique()
    contact_dict = _seed_dictionary(unique_ids)
    for i in range(len(contact_results)):
        contact = contact_results.iloc[i]
        contact_info = {
            'name': contact.contact_name,
            'phone': contact.contact_phone,
            'email': contact.contact_email,
            'website': contact.contact_website,
            'notes': contact.contact_notes,
        }
        contact_dict[contact.product_id] = contact_dict[contact.product_id] + [contact_info]
    return contact_dict


def split_field(results:str, delimiter:str, req_arr=False) -> list:
    """
        split_field
            Split a string on delimiter and format the output.
        Params:
        :resuts: (str) string to split
        :delimiter: (str) delimiter to split on
        :req_arr: (bool) 
    """
    def _check_valid_arr(arr:list):
        if len(arr) > 1:
            return arr
        else:
            try:
                return arr[0]
            except:
                return None

    if req_arr:
        return [x for x in results.split(delimiter) if len(x) > 1]
    else:
        return _check_valid_arr([x for x in results.split(delimiter) if len(x) > 1])
    