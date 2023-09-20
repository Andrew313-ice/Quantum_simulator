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
print(reduce(np.kron, ([np.eye(2)] +  [np.eye(2) * (2 - 1)])))


# I = np.eye(2)
# projection_operator = [reduce(np.kron, 
#                               [np.eye(2)] * (3 - 3) + \
#                               [(tmp:=np.eye(2)[:, i, None]) @ tmp.T.conjugate()] + \
#                               [np.eye(2)] * (3 - 1)
#                        ) for i in range(2)
# ]
# print(projection_operator[0])

print((tmp:=np.array([1, 1])) / np.linalg.norm(tmp))

GATE_DICT = {
    'rz':lambda theta:np.array([[np.exp(-1j*theta/2), 0                 ],
                                [0                  , np.exp(1j*theta/2)]])
}
print(callable(GATE_DICT['rz']))


def func():
    a = [1]
    # return a.append(2)
    return a.append(2)

print(func())
