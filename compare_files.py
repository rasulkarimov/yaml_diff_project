from yaml_diff import load_yaml_file, compare_dicts
from termcolor import colored

# Compares two YAML files and prints the differences
def print_diff(current_file, desired_file):
    current_state = load_yaml_file(current_file)
    desired_state = load_yaml_file(desired_file)
    
    removed, added, changed = compare_dicts(current_state, desired_state)
    
    print(f"Comparing files '{current_file}' and '{desired_file}':\n")
    
    if removed:
        print("The following items were removed:")
        for item in removed:
            print(colored(f"-  {item}", 'red')) 
    else:
        print("No items were removed.")
    
    if added:
        print("\nThe following items were added:")
        for item in added:
            print(colored(f"+  {item}", 'green'))
    else:
        print("\nNo items were added.")
    
    if changed:
        print("\nThe following items were changed:")
        for item in changed:
            print(colored(f"~  {item['path']}:", 'yellow'))
            print(colored(f"    old value: {item['old_value']}", 'red'))
            print(colored(f"    new value: {item['new_value']}", 'green'))
    else:
        print("\nNo items were changed.")
    
    print("\n" + "="*50 + "\n")

# Main function to compare multiple files
def main():
    print_diff('config_file_1.yaml', 'config_file_2.yaml')
    print_diff('config_file_2.yaml', 'config_file_3.yaml')
    print_diff('config_file_1.yaml', 'config_file_3.yaml')

if __name__ == "__main__":
    main()
