
from array import array

# Approach 1
# Using a magic number
NO_ENTITIES = 128
x = array('B', [101] * NO_ENTITIES)
y = array('B', [101] * NO_ENTITIES)

for i in range(NO_ENTITIES):
    if x[i] == 101:
        continue
    process() 

# Approach 2
# Using a boolean array
NO_ENTITIES = 128
b = array('B', [0] * NO_ENTITIES)
x = array('B', [0] * NO_ENTITIES)
y = array('B', [0] * NO_ENTITIES)

for i in range(NO_ENTITIES):
    if not b[i]:
        continue
    process() 

# Approach 3
# Dynamic arrays
NO_ENTITIES = 128
x = array('B')
y = array('B')

for i in range(len(x)):
    process()
