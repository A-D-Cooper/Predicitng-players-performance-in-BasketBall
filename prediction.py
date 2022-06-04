import numpy as np
from random import randint


def predict(lst, model):

    for r in range(len(lst)):
        arr = np.array([])
        for i in lst[r]:
            arr = np.append(arr, i.data.to_numpy())
            print((i.data.to_numpy()).shape)
            #print(arr.shape)
            arrl = arr.tolist()
            print(len(arrl))
            arr = np.pad(arrl, (0, 4980 - len(arrl)), 'constant')
            arr[np.isnan(arr)] = 0
            y = model(arr)
        for i in range(len(lst[r])):
            lst[r][i].pp = y[i]
    lst2 = []
    for r in lst:
        for i in r:
            lst2.append(i)
    #print(lst)
    return lst2
