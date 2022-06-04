import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import TimeoutException
import numpy as np
import pandas as pd
from constants import one_empty
from math import ceil
import io

wait_time = 30

driver = webdriver.Chrome("C:/SeleniumDrivers/chromedriver.exe")


def login():
    username = "AD1999"
    password = "Iamdbcooper1971"
    driver.get("https://stathead.com/users/login.cgi")
    driver.implicitly_wait(30)

    usernm_txt = driver.find_element_by_id("username")
    pas_txt = driver.find_element_by_id("password")

    usernm_txt.send_keys(username)
    pas_txt.send_keys(password)

    sub_btn = driver.find_element_by_id("sh-login-button")
    sub_btn.click()


def convert_to_csv():
    driver.implicitly_wait(wait_time)
    try:
        menu = driver.find_element_by_xpath(
            '//*[@id="stats_sh"]/div/ul/li[1]/span')  # //*[@id="stats_sh"]/div/ul/li[1]/span, //*[@id="stats_sh"]/div/ul/li[1]/span

    except NoSuchElementException:
        time.sleep(wait_time)
        driver.refresh()
        try:
            menu = driver.find_element_by_xpath('//*[@id="stats_sh"]/div/ul/li[1]/span')

        except NoSuchElementException:
            try:
                time.sleep(wait_time)
                driver.refresh()
                menu = driver.find_element_by_xpath('//*[@id="stats_sh"]/div/ul/li[1]/span')

            except NoSuchElementException:
                return 1

    action = ActionChains(driver)
    action.move_to_element(menu)
    csv_btn = driver.find_element_by_xpath(
        '//*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button')  # //*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button  //*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button
    action.move_to_element(csv_btn)
    action.click().perform()
    return 0


def get_player_data(player):
    player_page = "https://stathead.com/basketball/pgl_finder.cgi"
    driver.get(player_page)
    search_box = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/input[2]")
    search_box.send_keys(player)
    search_btn = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div[2]/div[1]/div[4]/div/input")
    search_btn.click()



def next_btn(link_url, i):
    strng = ''

    last_page = False
    f_line = True
    while not last_page:
        driver.implicitly_wait(wait_time)
        try:
            driver.get(link_url)
        except TimeoutException:
            try:
                driver.refresh()
                driver.get(link_url)
            except TimeoutException:
                driver.refresh()
                driver.get(link_url)

        html_source = driver.page_source
        r = convert_to_csv()
        if r==1:
            return strng
        strng = str_concat(strng, f_line)

        f_line = False

        soup = BeautifulSoup(html_source, 'lxml')
        links = soup.find_all('div', class_='prevnext')

        for link in links:
            l = link.find_all('a', class_='button2 next')
            if len(l) == 0:
                last_page = True
            else:
                link_url = "https://stathead.com" + l[0]['href']
    #pre_file.close()
    return strng


def str_concat(strng, f_line):

    driver.implicitly_wait(wait_time)

    data_in_str = driver.find_element_by_xpath('//*[@id="csv_stats"]').text  #//*[@id="csv_stats"]/text()[2]  //*[@id="csv_stats"]/text()[2]

    if f_line:
        first_line = data_in_str.find('\n') + 1
        second_line = data_in_str.find('\n', first_line) + 1
        third_line = data_in_str.find('\n', second_line) + 1
        fourth_line = data_in_str.find('\n', third_line) + 1
        #fifth_line = data_in_str.find('\n', fourth_line) + 1

        #imd = data_in_str[fourth_line:] + '\n'

        #pre_file.write(imd)

        concat_str = strng + data_in_str[fourth_line:] + '\n'

        #print(data_in_str[fourth_line:])


        #print(first_line, second_line, third_line, fourth_line, fifth_line)

    else:
        first_line = data_in_str.find('\n') + 1
        second_line = data_in_str.find('\n', first_line) + 1
        third_line = data_in_str.find('\n', second_line) + 1
        fourth_line = data_in_str.find('\n', third_line) + 1
        fifth_line = data_in_str.find('\n', fourth_line) + 1
        #sixth_line = data_in_str.find('\n', fifth_line) + 1

        imd = data_in_str[fifth_line:] + '\n'

        #pre_file.write(imd)

        concat_str = strng + data_in_str[fifth_line:] + '\n'

        #print(data_in_str[fifth_line:])
        #print(first_line, second_line, third_line, fourth_line, fifth_line, sixth_line)

    return concat_str


def proc_player_data(player_rec, date):


    player_rec = player_rec.replace({'%': ''}, regex=True)
    #player_rec = player_rec.drop(['dt'], axis=1)

    #player_rec['Date'] = pd.to_datetime(player_rec.Date)
    player_rec.sort_values('Date', ascending=False)

    #player_record_to_date = player_rec[player_rec['Date'] < date]
    #this_game = player_rec[player_rec['Date'] == date]
    m, n = player_rec.shape

    this_game = pd.DataFrame([''])
    fp = this_game.iloc[0, :5].to_frame().T
    fp['games played'] = m

    avg = (player_rec.iloc[:, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
    avg.columns = avg.columns + '_avg'

    fp2 = this_game.loc[:, 'dk_f'].reset_index(drop=True)
    fp2.rename('dkf_t', inplace=True)
    fp2 = fp2.fillna(0)
    fp = pd.concat([fp.reset_index(drop=True), fp2.reset_index(drop=True)], axis=1, join='outer')

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
        last_five = (player_rec.iloc[0:5, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = pd.DataFrame(one_empty, index=[0])
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = pd.DataFrame(one_empty, index=[0])
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 4 < m < 11:
        last_five = (player_rec.iloc[0:5, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = pd.DataFrame(one_empty, index=[0])
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m * 0.1), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 10 < m < 51:
        last_five = (player_rec.iloc[0:5, 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        last_five.columns = last_five.columns + '_5'

        one_perc = pd.DataFrame(one_empty, index=[0])
        one_perc.columns = one_perc.columns + '_1%'

        five_perc = (player_rec.iloc[0:ceil(m * 0.05), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        five_perc.columns = five_perc.columns + '_5%'

        ten_perc = (player_rec.iloc[0:ceil(m * 0.1), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        ten_perc.columns = ten_perc.columns + '_10%'

        tf_perc = (player_rec.iloc[0:ceil(m * 0.25), 5:32].apply(pd.to_numeric).fillna(0).mean()).to_frame().T
        tf_perc.columns = tf_perc.columns + '_25%'

        final = pd.concat([fp.reset_index(drop=True), last_five.reset_index(drop=True), one_perc.reset_index(drop=True), five_perc.reset_index(drop=True),
             ten_perc.reset_index(drop=True), tf_perc.reset_index(drop=True), avg.reset_index(drop=True)], axis=1, join='outer')

    if 50 < m:
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

            for player in tm1_lst[1:]:

                player_rec = pd.read_csv('player files\\' + player + '.csv')

                frame = proc_player_data(player_rec, date)

                final_data.reset_index(inplace=True, drop=True)

                final_data = pd.concat([final_data.reset_index(drop=True), frame.reset_index(drop=True)], axis=0)  #.drop_duplicates()

            final_data.to_csv('appended data\\' + str(counter) + '.csv')
            counter +=1


def write_to_csv():
    #url_lst = url_ls()

    #'https://stathead.com/basketball/pgl_finder.cgi?request=1&match=game&order_by_asc=0&order_by=pts&year_min=1991&year_max=2022&is_playoffs=N&lg_id=NBA&age_min=0&age_max=99&season_start=1&season_end=-1'

    url_lst = [
        'https://stathead.com/hockey/pgl_finder.cgi?request=1&match=game&group_set=single&order_by_asc=0&order_by=goals&year_min=1991&year_max=2022&is_playoffs=N&age_min=0&age_max=99&season_start=1&season_end=-1&pos=S'
        ]


    file_n = 'SH basketball data'
    counter = 2
    for u in url_lst:
        strng = next_btn(u, counter)
        file_name = file_n + ' ' + str(counter) + '.csv'
        file = open(file_name, 'w+', encoding="utf-8")
        file.write(strng)
        file.close()
        counter += 1



if __name__ == "__main__":
    login()


