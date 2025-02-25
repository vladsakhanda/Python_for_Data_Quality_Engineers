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
rInt = lambda start, end: random.randint(start, end)

ls = [
      {
            chr(rInt(97, 122)): rInt(0, 100),
            chr(rInt(97, 122)): rInt(0, 100),
            chr(rInt(97, 122)): rInt(0, 100)
       }
      for j in range(rInt(2, 10))
]

print(ls)

'''
2. get previously generated list of dicts and create one common dict:

if dicts have same key, we will take max value, and rename key with dict number with max value
if key is only in one dict - take it as is,
example:{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
Each line of code should be commented with description.
'''
# ls1 = [{'1':1},{'1':2}]
# commonDict = {}
# for d in ls1:
#       print(d)
#       if
