import random

def generate_random_dict():
    """Generate a dictionary with random keys (letters) and random values (numbers 0-100)."""
    keys_count = random.randint(2, 10)
    keys = random.sample('abcdefghijklmnopqrstuvwxyz', keys_count)
    return {key: random.randint(0, 100) for key in keys}

def create_dict_list(count):
    """Create a list of random number of dictionaries."""
    return [generate_random_dict() for _ in range(random.randint(2, count))]

def prettify_print(lst):
    """Print list elements in a more structured format."""
    print('[')
    for d in lst:
        print(d)
    print(']\n')

def merge_dictionaries(dict_list):
    """Merge dictionaries to form a new dictionary based on specified rules."""
    result_dict = {}
    for index, current_dict in enumerate(dict_list):
        for key, value in current_dict.items():
            new_key = f"{key}_{index + 1}"
            if key in result_dict:
                if result_dict[key][1] < value:
                    result_dict[key] = (new_key, value)
            else:
                result_dict[key] = (new_key, value)

    return {k if v[0] == k else v[0]: v[1] for k, v in result_dict.items()}

# Main Execution
if __name__ == "__main__":
    list_of_dicts = create_dict_list(10)
    prettify_print(list_of_dicts)
    merged_dict = merge_dictionaries(list_of_dicts)
    print(merged_dict)