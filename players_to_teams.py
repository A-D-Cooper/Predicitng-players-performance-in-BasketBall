import pickle
import pandas as pd
from constants import one_empty
from math import ceil



def player_to(lst):
    teams = []
    opp = []
    for i in lst:
        if i.tm not in teams:
            teams.append(i.tm)
            teams.append(i.opp)
            opp.append((i.tm, i.opp))
    l = []
    for r in range(len(opp)):
        l.append([])
        for i in lst:
            if i.tm == opp[r][0]:
                l[r].insert(0, i)
            if i.tm == opp[r][1]:
                l[r].append(i)
    return l





def proc_player_data(p):
    player_rec = p.data

    load_file = open('Positions_3.pickle', 'rb')
    positions = pickle.load(load_file)
    load_file2 = open('Teams_emb.pickle', 'rb')
    teams = pickle.load(load_file2)


    player_rec = player_rec.replace({'%': ''}, regex=True)

    player_rec['Date'] = pd.to_datetime(player_rec.Date)
    player_rec.sort_values('Date', ascending=False)


    age = player_rec['Age'].str.split('-', expand=True)
    age = pd.to_numeric(age.iloc[:, 0]) + pd.to_numeric(age.iloc[:, 1]) / 365

    m, n = player_rec.shape

    tem = p.tm
    if tem not in teams.keys():
        #teams[tem] = len(positions.keys()) + 1
        #pickle.dump(positions, open('Teams_emb.pickle', 'wb'))
        print(tem)


    fp = pd.DataFrame({'Age': age, 'Pos': positions[p.p_pos], 'games played': m, 'Tm': teams[p.tm], 'Opp': teams[p.opp]})

    avg = (player_rec.iloc[:, 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
    avg.columns = avg.columns + '_avg'

    if m == 0:
        last_five = pd.DataFrame(one_empty, index=[0])
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = pd.DataFrame(one_empty, index=[0])
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = pd.DataFrame(one_empty, index=[0])
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = pd.DataFrame(one_empty, index=[0])
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 0 < m < 5 :
        last_five = (player_rec.iloc[0:5, 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = pd.DataFrame(one_empty, index=[0])
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = pd.DataFrame(one_empty, index=[0])
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 4 < m < 11:
        last_five = (player_rec.iloc[0:5, 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = pd.DataFrame(one_empty, index=[0])
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m * 0.1), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 10 < m < 51:
        last_five = (player_rec.iloc[0:5, 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = (player_rec.iloc[0:ceil(m * 0.05), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m * 0.1), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 50 < m:
        last_five = (player_rec.iloc[0:5, 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = (player_rec.iloc[0:ceil(m*0.01), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = (player_rec.iloc[0:ceil(m*0.05), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m*0.1), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m*0.25), 7:33].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True), ten_perc.reset_index(drop=True),
                        tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')


    print("final shape ", final.shape)
    return final


def to_np():
    data = []

    load_file = open('Pos_emb.pickle', 'rb')
    positions = pickle.load(load_file)
    load_file2 = open('Teams_emb.pickle', 'rb')
    teams = pickle.load(load_file2)

    max = 0

    path = 'full matches\\'
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