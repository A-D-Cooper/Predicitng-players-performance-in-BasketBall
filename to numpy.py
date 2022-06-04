import numpy as np
import pandas as pd
import os
import pickle
import time


def to_np():
    data = [[], []]

    load_file = open('Positions_2.pickle', 'rb')
    positions = pickle.load(load_file)
    load_file2 = open('Teams_emb.pickle', 'rb')
    teams = pickle.load(load_file2)

    max = 0

    path = 'appended data\\'
    for filename in os.listdir(path):
        df1 = pd.read_csv(path + filename)

        m, n = df1.shape
        if m > max:
            max = m

        target = df1['dkf_t'].to_numpy()
        df1.drop(['Opp', 'Date', 'Unnamed: 0', 'dkf_t'], axis=1, inplace=True)
        age = df1['Age'].str.split('-', expand=True)
        df1['Age'] = pd.to_numeric(age.iloc[:, 0]) + pd.to_numeric(age.iloc[:, 1]) / 365

        tm_list = list(teams.keys())
        for t in tm_list:
            df1['Tm'] = df1['Tm'].replace([t], teams[t])

        ps_list = list(positions.keys())
        for t in ps_list:
            df1['Pos'] = df1['Pos'].replace([t], positions[t])

        df1['Tm'] = pd.to_numeric(df1['Tm'])
        df1['Pos'] = pd.to_numeric(df1['Pos'])

        arr = df1.to_numpy()
        arr = arr.flatten()

        data[0].append(arr)
        data[1].append(target)

    print('max rows:  ', max)

    #np_data1 = np.array(data[0], dtype=np.float64)
    #np_data2 = np.array(data[1], dtype=np.float64)
    #np.save('numpy_data.npy', np_data1)
    #np.save('np_target.npy', np_data2)
    print(data)
    with open('data_list.pickle', 'wb') as f1:
        pickle.dump(data, f1, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    start = time.time()
    to_np()
    print('Time: ', time.time() - start)
