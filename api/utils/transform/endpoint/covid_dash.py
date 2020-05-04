import pandas as pd

def condense_sponsors(sponsor_results):
    # Requires sponsors in the form (product_id, sponsor_id, sponsor_name)
    print(f'incoming type: {type(sponsor_results)}')
    unique_ids = sorted(list(set([result[0] for result in sponsor_results])))
    sponsor_dict= {}
    [sponsor_dict.update({unique_id:[]}) for unique_id in unique_ids]
    for result in sponsor_results:
        prod_id = result[0]
        spon_id = result[1]
        spon_name = result[2]
        sponsor_info = {'sponsorId': spon_id, 'sponsorName': spon_name}
        sponsor_dict[prod_id] = sponsor_dict[prod_id] + [sponsor_info]
    return sponsor_dict


def _clean_date(date):
    if pd.isnull(date):
        return None
    return date

def condense_milestones(milestone_results: pd.DataFrame) -> dict:
    unique_ids = milestone_results.product_id.unique()
    print(f'Length Results = {len(milestone_results)}')
    milestone_dict = {}
    [milestone_dict.update({unique_id:[]}) for unique_id in unique_ids]
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


def fetch_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return []