from yaml_diff import load_yaml_file, compare_dicts
from termcolor import colored

# Compares two YAML files and prints the differences
def print_diff(current_file, desired_file):
    # Load the YAML files
    current_state = load_yaml_file(current_file)
    desired_state = load_yaml_file(desired_file)
    
    # Perform the comparison
    removed, added, changed = compare_dicts(current_state, desired_state)
    
    print(f"Comparing files '{current_file}' and '{desired_file}':\n")
    
    # Handle removed items
    if removed:
        print("The following items were removed:")
        for item in removed:
            for key, value in item.items():
                print(colored(f"- {key}:", "red"))
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(colored(f"  {sub_key}: {sub_value}", "red"))
                elif isinstance(value, list):
                    for sub_item in value:
                        if isinstance(sub_item, dict):
                            for sub_key, sub_value in sub_item.items():
                                print(colored(f"  {sub_key}: {sub_value}", "red"))
    else:
        print("No items were removed.")
    
    # Handle added items
    if added:
        print("\nThe following items were added:")
        for item in added:
            for key, value in item.items():
                print(colored(f"+ {key}:", "green"))
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(colored(f"  {sub_key}: {sub_value}", "green"))
    else:
        print("\nNo items were added.")
    
    # Handle changed items
    if changed:
        print("\nThe following items were changed:")
        for item in changed:
            print(colored(f"~ {item['path']}:","yellow"))
            print(colored(f"  old value: {item['old_value']}","yellow"))
            print(colored(f"  new value: {item['new_value']}","yellow"))
    else:
        print("\nNo items were changed.")
    
    print("\n" + "="*50 + "\n")

def main():
    print_diff('config_file_1.yaml', 'config_file_2.yaml')
    print_diff('config_file_2.yaml', 'config_file_3.yaml')
    print_diff('config_file_1.yaml', 'config_file_3.yaml')

if __name__ == "__main__":
    main()
