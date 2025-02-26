'''
Each line of code should be commented with description.
Commit script to git repository and provide link as home task result.
'''
import random

# Create list of 100 random numbers from 0 to 1000
ls = [random.randint(0, 1000) for x in range(100)]
ls_sorted = []
print(ls)

# Sort list from min to max(without using sort())
# I've decided to choose selection sort O(n^2) because it is simple and works well on small lists
while len(ls) > 0:
    # Select and remove minimum element from ls and append to lsSorted
    ls_sorted.append(ls.pop(ls.index(min(ls))))

print('ls:', ls)
print('lsSorted:', ls_sorted)

''' Calculate average for even and odd numbers
print both average result in console '''
# Variables' initialization
even_sum = even_count = odd_sum = odd_count = 0
for i in range(len(ls_sorted)):
    current_number = ls_sorted[i]
    if current_number % 2 == 0:
        even_sum += current_number
        even_count += 1
    else:
        odd_sum += current_number
        odd_count += 1

if even_count != 0:
    print('Average for even numbers', even_sum / even_count)
else:
    print('No even numbers')

if odd_count != 0:
    print('Average for odd numbers', odd_sum / odd_count)
else:
    print('No odd numbers')
