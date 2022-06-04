import pandas as pd
import os
import time
from constants import one_empty
import numpy as np
from math import ceil


def player_data(file):
    data = pd.read_csv(file, low_memory=False)
    player_name_id = data['Player'].str.split('\\', expand=True)
    data['player_name'] = player_name_id.loc[:, 0]
    data['player_id'] = player_name_id.loc[:, 1]
    prep_data = data.drop(['Rk', 'Player', 'Unnamed: 6', 'Unnamed: 8'], axis=1)
    player_ids = pd.unique(prep_data['player_id'])

    start1 = time.time()
    counter = 0
    print(player_ids.shape)
    for p_id in player_ids:
        single_player_data = prep_data[prep_data['player_id'] == p_id]
        print(single_player_data)
        single_player_data.to_csv('player files\\' + p_id + '.csv', index=False)
        counter +=1
        if counter == 10:
            end1 = time.time()
            print(start1 - end1)

def add_dff(file):

    df1 = pd.read_csv(file, low_memory=False)
    #df1 = df1.drop(['Unnamed: 0'], axis=1)
    df1.loc[:, 'dk_f'] = 0
    df1.loc[:, 'dt'] = 0
    m, n = df1.shape
    for i in range(m):
        dt = 0
        if df1.iloc[i, 9] > 9:
            dt += 1
        if df1.iloc[i, 27] > 9:
            dt += 1
        if df1.iloc[i, 28] > 9:
            dt += 1
        if df1.iloc[i, 29] > 9:
            dt += 1
        if df1.iloc[i, 30] > 9:
            dt += 1

        if dt == 2:
            df1.iloc[i, 35] = 1.5
        if dt > 2:
            df1.iloc[i, 35] = 3

    df1['dk_f'] = df1['PTS'] + (df1['3P'] * 0.5) + (df1['TRB'] * 1.25) + (df1['AST'] * 1.5) + (df1['STL'] * 2) + (df1['BLK'] * 2) + (df1['TOV'] * -0.5) + df1['dt']
    df1.to_csv('mod 1.csv', index=False)


def match_data(file):
    df1 = pd.read_csv(file, low_memory=False)

    player_name_id = df1['Player'].str.split('\\', expand=True)
    df1['player_name'] = player_name_id.loc[:, 0]
    df1['player_id'] = player_name_id.loc[:, 1]
    df1 = df1.drop(['Rk', 'Player', 'Unnamed: 6', 'Unnamed: 8'], axis=1)

    df1['tm_key'] = df1['Date'].astype(str) + df1['Tm']
    df1['opp_key'] = df1['Date'].astype(str) + df1['Opp']
    mat = pd.unique(df1['tm_key'])
    for m in mat:
        match = df1[df1['tm_key'] == m]
        match.to_csv('match files\\' + m + '.csv', index=False)


def proc_player_data(player_rec, date):

    #player_rec = player_rec.drop(['Unnamed: 0'], axis=1)
    player_rec = player_rec.replace({'%': ''}, regex=True)
    player_rec = player_rec.drop(['dt'], axis=1)

    player_rec['Date'] = pd.to_datetime(player_rec.Date)
    player_rec.sort_values('Date', ascending=False)
    #print(date)
    player_record_to_date = player_rec[player_rec['Date'] < date]
    this_game = player_rec[player_rec['Date'] == date]
    m, n = player_record_to_date.shape

    #print()

    fp = this_game.iloc[0, :5].to_frame().T
    fp['games played'] = m
    last_game = player_rec.iloc[0, 5:32].fillna(0).to_frame().T
    avg = (player_rec.iloc[:, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T

    avg.columns = avg.columns + '_avg'

    fp2 = this_game.loc[:, 'dk_f'].reset_index(drop=True)
    fp2.rename('dkf_t', inplace=True)
    fp2 = fp2.fillna(0)
    fp = pd.concat([fp.reset_index(drop=True), fp2.reset_index(drop=True)], axis=1, join='outer')


    #print('m is   ',  m)
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

    else:
        last_five = (player_rec.iloc[0:5, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = (player_rec.iloc[0:ceil(m*0.01), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = (player_rec.iloc[0:ceil(m*0.05), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m*0.1), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m*0.25), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True), ten_perc.reset_index(drop=True),
                        tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    return final


def full_match(path):

    path2 = 'player matches'
    read_files = []
    counter = 1
    for filename in os.listdir(path):
        if filename not in read_files:
            tm1 = pd.read_csv(path + filename)
            #print(tm1.shape)
            file2 = path + tm1.iloc[0,36] + '.csv'
            tm2 = pd.read_csv(file2)

            #TODO: Add the column no. of date
            date = tm1.iloc[1, 2]

            # Marking the read files
            read_files.append(filename)
            read_files.append(file2)

            # Getting the ids of players on both teams into a list
            tm1_lst = tm1['player_id'].tolist()
            tm2_lst = tm2['player_id'].tolist()
            tm1_lst.extend(tm2_lst)

            # reaidng file of first player
            p1 = pd.read_csv('player files\\' + tm1_lst[0] + '.csv')

            final_data = proc_player_data(p1, date)

            #final_data = final_data.to_frame().T
            #counter2 =1
            for player in tm1_lst[1:]:

                player_rec = pd.read_csv('player files\\' + player + '.csv')
                #print(player)

                frame = proc_player_data(player_rec, date)
                #print(frame.columns, '\n \n brak \n \n', final_data.columns)

                #frame = frame.to_frame().T
                final_data.reset_index(inplace=True, drop=True)
                #frame = frame.reset_columns()
                #print(final_data.shape, frame.shape)

                final_data = pd.concat([final_data.reset_index(drop=True), frame.reset_index(drop=True)], axis=0)  #.drop_duplicates()

            final_data.to_csv('full matches\\' + str(counter) + '.csv')
            counter +=1




if __name__ == '__main__':
    #file_loc = 'combines data.csv'
    #add_dff('SH basketball data 1.csv')
    #player_data('mod 1.csv')
    #match_data('mod 1.csv')
    full_match('match files\\')

