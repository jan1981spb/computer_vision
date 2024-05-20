import numpy as np
from minisom import MiniSom
from sklearn.preprocessing import MinMaxScaler

arr = [(8,4,17), (21,3,18), (6,7,20), (2,5,18), (23,18,25),
       (24,18,17), (25,21,16), (2,24,18), (6,20, 24), (2,21,22),
       (8,19,17), (1,24,20), (3,2,21), (22,2,19), (19,4,23),
       (20,7,17), (24,19,18), (2,6,19), (23,8,25), (18,16,22),
       (3,24,23), (18,3,21), (21,25,22), (5,3,24), (24,17,21)]

data = np.array(arr)

sc = MinMaxScaler(feature_range = (0,1))
sc.fit(data)
X=sc.transform(data)
type(X)

som = MiniSom(x = 4, y = 4, input_len = 3, sigma=0.1, learning_rate=0.9)
som.random_weights_init(X)
som.train(data, 100)

winers = {}
for x in X:
    win = som.winner(x)
    if (winers.get(win[1]) is None):
        winers[win[1]] = [win[0]]
    else:
        subarr =  winers[win[1]]
        subarr.append(win[0])
        winers[win[1]] = subarr


print("Кластеры со значениями групп элементов")

for output in winers:
    print(f'Кластер {output}')
    print(f'Значения {winers[output]}')
