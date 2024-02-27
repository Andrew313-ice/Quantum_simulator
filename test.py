import numpy as np
import array

def func():
    return array.array('b', [1, 2, 3]), array.array('b', [1, 2, 3])

print(type(func()[0]))