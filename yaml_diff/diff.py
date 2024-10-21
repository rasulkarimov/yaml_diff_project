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
            if isinstance(current[key], list):
              current_value = current[key]
              desired_value = []
              rem, add, chg = compare_lists(current_value, desired_value, f"{path}.{key}")
              removed.extend(rem)
              added.extend(add)
              changed.extend(chg)
            else:
              removed.append({f"{path}.{key}": current[key]})
            
    for key in desired:
        if key not in current:
          if isinstance(desired[key], list):
            current_value = []
            desired_value = desired[key]
            rem, add, chg = compare_lists(current_value, desired_value, f"{path}.{key}")
            removed.extend(rem)
            added.extend(add)
            changed.extend(chg)
          else:
            added.append({f"{path}.{key}": desired[key]})

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

    # Convert the lists into dictionaries using the first field (unique key) for comparison
    current_dict = {item[next(iter(item))]: item for item in current_list}
    desired_dict = {item[next(iter(item))]: item for item in desired_list}

    # Compare the current and desired dicts (which represent the lists)
    for key in current_dict:
        if key not in desired_dict:
            # Format path to show list elements like containers[nginx]
            removed.append({f"{path}[{key}]": current_dict[key]})
    for key in desired_dict:
        if key not in current_dict:
            added.append({f"{path}[{key}]": desired_dict[key]})
    for key in current_dict:
        if key in desired_dict:
            current_value = current_dict[key]
            desired_value = desired_dict[key]

            # If both are dictionaries, recurse into them
            if isinstance(current_value, dict) and isinstance(desired_value, dict):
                rem, add, chg = compare_dicts(current_value, desired_value, f"{path}[{key}]")
                removed.extend(rem)
                added.extend(add)
                changed.extend(chg)

            # If values are different, it's a change
            elif current_value != desired_value:
                changed.append({
                    'path': f"{path}[{key}]",
                    'old_value': current_value,
                    'new_value': desired_value
                })
    
    return removed, added, changed