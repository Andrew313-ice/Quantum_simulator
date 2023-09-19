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

n = 0
for i in range(1000):
    n += np.random.choice([0, 1])
print(n / 1000)

print(type(np.eye(2).shape[0]))
