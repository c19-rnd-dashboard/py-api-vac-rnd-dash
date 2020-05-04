def condense_sponsors(sponsor_results):
    # Requires sponsors in the form (product_id, sponsor_id, sponsor_name)
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


def condense_milestones(milestone_results):
    # Requires milestones in the form (product_id, milestone_id, date, status, name, category)
    unique_ids = sorted(list(set([result[0] for result in milestone_results])))
    print(f'Length Results = {len(milestone_results)}')
    milestone_dict = {}
    [milestone_dict.update({unique_id:[]}) for unique_id in unique_ids]
    for result in milestone_results:
        prod_id = result[0]
        milestone_id = result[1]
        date = result[2]
        status = result[3]
        name = result[4]
        category = result[5]
        milestone_info = {
            'milestoneId': milestone_id,
            'name': name,
            'category': category,
            'date': date,
            'status': status,
            
        }
        milestone_dict[prod_id] = milestone_dict[prod_id] = [milestone_info]
    return milestone_dict


def fetch_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return []