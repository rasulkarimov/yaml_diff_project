import yaml

# Load a YAML file and return a dictionary
def load_yaml_file(file_path: str):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Recursively compares two dictionaries and returns differences
def compare_dicts(current, desired, path: str = ""):
    removed, added, changed = [], [], []
    
    for key in current:
        if key not in desired:
            removed.append(f"{path}.{key}")
            
    for key in desired:
        if key not in current:
            added.append(f"{path}.{key}")

    for key in current:
        if key in desired:
            current_value = current[key]
            desired_value = desired[key]

            if isinstance(current_value, dict) and isinstance(desired_value, dict):
                rem, add, chg = compare_dicts(current_value, desired_value, f"{path}.{key}")
                removed.extend(rem)
                added.extend(add)
                changed.extend(chg)

            elif isinstance(current_value, list) and isinstance(desired_value, list):
                rem, add, chg = compare_lists(current_value, desired_value, f"{path}.{key}")
                removed.extend(rem)
                added.extend(add)
                changed.extend(chg)

            elif current_value != desired_value:
                changed.append({
                    'path': f"{path}.{key}",
                    'old_value': current_value,
                    'new_value': desired_value
                })

    return removed, added, changed

# Compare two lists of dictionaries using the first field as the unique key
def compare_lists(current_list, desired_list, path: str):
    removed, added, changed = [], [], []

    current_dict = {item[next(iter(item))]: item for item in current_list}
    desired_dict = {item[next(iter(item))]: item for item in desired_list}

    rem, add, chg = compare_dicts(current_dict, desired_dict, path)
    
    removed.extend(rem)
    added.extend(add)
    changed.extend(chg)
    
    return removed, added, changed
