'''
Commit script to git repository and provide link as home task result.
'''
import random

''' 
1. create a list of random number of dicts (from 2 to 10)
dict's random numbers of keys should be letter,
dict's values should be a number (0-100),
example:[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
'''
ls = list()
for i in range(random.randint(2, 10)):
    available_letters = [chr(i) for i in list(range(97, 123))]  # Creating list of available letters and reseting on each iteration
    current_dict = dict()  # New dict
    for j in range(random.randint(2, 10)):
        current_dict[
            available_letters.pop(
                available_letters.index(
                    random.choice(available_letters)
                )

            )
        ] = random.randint(0, 100)

    ls.append(current_dict)  # Adding our dict to list

print('[')
prettified_output = [print(d) for d in ls] # Funny way to print something using comprehensions :)
print(']\n')

'''
2. get previously generated list of dicts and create one common dict:

if dicts have same key, we will take max value, and rename key with dict number with max value
if key is only in one dict - take it as is,
example:{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
Each line of code should be commented with description.
'''
res = dict()
ignoring_letters_list = []
for i in range(len(ls)):
    for j in ls[i]:
        current_letter = str(j)

        if current_letter not in ignoring_letters_list:
            current_dict = {i + 1: ls[i][j]}
            ignoring_letters_list.append(current_letter)

            for k in range(i + 1, len(ls)):
                for m in ls[k]:
                    if j == m:
                        current_dict[k + 1] = ls[k][m]

            if len(current_dict) < 2:
                res[str(j)] = ls[i][j]
            else:
                number_of_dict = max_value = max(current_dict.values())
                for key, value in current_dict.items():
                    if max_value == value:
                        number_of_dict = key
                        res[f'{j}_{key}'] = max_value
                        break

print(res)
