import numpy as np
from functools import reduce

dic_fun = {'a':lambda x:print(x)}

dic_fun['a'](100)

try:
    print(dic_fun['c'])
except KeyError:
    print("No")


if not None:
    print('None')

print(np.eye(2)[[1, 0], :])

a = np.zeros((2**2, 1))
a[0, 0] = 1
print(reduce(np.kron, [np.eye(2)] +  [np.eye(2) * (2 - 1)]))


