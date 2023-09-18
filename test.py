
dic_fun = {'a':lambda x:print(x)}

dic_fun['a'](100)

try:
    print(dic_fun['c'])
except KeyError:
    print("No")


if not None:
    print('None')