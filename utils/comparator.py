

def compare_dicts(previous_data:dict, new_data:dict):
    '''use to get difference between to dictionary'''
    # Find keys that are common to both dictionaries
    common_keys = set(previous_data.keys()) & set(new_data.keys())

    # Find keys that are unique to each dictionary
    unique_keys_dict1 = set(previous_data.keys()) - set(new_data.keys())
    unique_keys_dict2 = set(new_data.keys()) - set(previous_data.keys())

    # Find values that are different for common keys
    diff_val = [(key, previous_data[key], new_data[key]) for key in common_keys if previous_data[key] != new_data[key]]

    # Create a dictionary of the differences
    differences = {
        'common_keys': common_keys,
        'unique_keys_dict1': unique_keys_dict1,
        'unique_keys_dict2': unique_keys_dict2,
        'different_values': diff_val
    }

    return differences

def get_diff_val(previous_data:dict, new_data:dict) -> list[tuple]:
    '''same as compare_dicts '''
    
    # Find keys that are common to both dictionaries
    common_keys = set(previous_data.keys()) & set(new_data.keys())

    # Find values that are different for common keys
    diff_vals = []
    for key in common_keys:
        if previous_data[key] != new_data[key]:
            diff_vals.append((key, previous_data[key], new_data[key]))

    return diff_vals


def is_diff(dict1, dict2) -> bool:
    '''check if two dictionary are same or not'''

    # Check for changes in keys
    if set(dict1.keys()) != set(dict2.keys()):
        return True

    # Check for changes in values
    for key in dict1:
        if dict1[key] != dict2[key]:
            return True

    # No changes detected
    return False