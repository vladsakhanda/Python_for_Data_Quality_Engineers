'''
Each line of code should be commented with description.
Commit script to git repository and provide link as home task result.
'''
import random

# Create list of 100 random numbers from 0 to 1000
ls = [random.randint(0, 1000) for x in range(100)]
lsSorted = []
print(ls)

# Sort list from min to max(without using sort())
# I've decided to choose selection sort O(n^2) because it is simple and works well on small lists
while len(ls) > 0:
    # Select and remove minimum element from ls and append to lsSorted
    lsSorted.append(ls.pop(ls.index(min(ls))))

print('ls:', ls)
print('lsSorted:', lsSorted)

''' Calculate average for even and odd numbers
print both average result in console '''
# Variables' initialization
evenSum = 0; evenCount = 0; oddSum = 0; oddCount = 0
for i in range(len(lsSorted)):
    currentNumber = lsSorted[i]
    if currentNumber % 2 == 0:
        evenSum += currentNumber
        evenCount += 1
    else:
        oddSum += currentNumber
        oddCount += 1

print('Average for even numbers', evenSum / evenCount)
print('Average for odd numbers', oddSum / oddCount)
