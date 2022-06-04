from player_class import player
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
#from pandas.compat import StringIO
from io import StringIO
from players_to_teams import proc_player_data
from players_to_teams import player_to
from prediction import predict
from player_class import algo
from pandas.errors import EmptyDataError
import pickle
from tensorflow import keras


#from scraper import login

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



def read_file(file=''):
    #file = "dks.csv"
    df = pd.read_csv(file)
    m, n = df.shape
    players = []

    for i in range(m):
        tmopp = df.iloc[i, 6].split(' ')[0].split('@')
        #p = player(df.iloc[i, 2], df.iloc[i, 5], -1, df.iloc[i, 4], data=None, p_pos=df.iloc[i, 0], tm=tmopp[0], opp=tmopp[1])
        p = player(df.iloc[i, 2], df.iloc[i, 5], df.iloc[i, -1], df.iloc[i, 4], data=None, p_pos=df.iloc[i, 0], tm=tmopp[0], opp=tmopp[1])
        players.append(p)
        #break
    login()
    players2 = []
    for i in players:
        data = get_data(i.name)
        if type(data) == int:
            print("1 missing player", i.name)
            continue
        i.data = data
        i.data = proc_player_data(i)
        players2.append(i)

    return players2



def get_data(p_name):
    r = get_page(p_name)
    if r==1:
        return 1
    strng = next_btn()
    try:
        df = pd.read_csv(StringIO(strng), sep=',')
    except EmptyDataError:
        return 1
    return df



def get_page(player):
    player_page = "https://stathead.com/basketball/pgl_finder.cgi"
    driver.get(player_page)
    search_box = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/input[2]")
    search_box.send_keys(player)
    driver.maximize_window()

    #search_btn = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div[2]/div[1]/div[4]/div/input")
    #search_btn = driver.find_element_by_class_name("sh-get-results")
    try:
        search_rslt = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/form/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/div/div/div/div[1]/div/span[2]')

    except NoSuchElementException:
        return 1

    search_rslt.click()
    search_btn = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/form/div[2]/div[2]/div[2]/p[2]/input')
    search_btn.click()



def str_concat(strng, f_line):

    driver.implicitly_wait(wait_time)

    data_in_str = driver.find_element_by_xpath('//*[@id="csv_stats"]').text  #//*[@id="csv_stats"]/text()[2]  //*[@id="csv_stats"]/text()[2]

    if f_line:
        first_line = data_in_str.find('\n') + 1
        second_line = data_in_str.find('\n', first_line) + 1
        third_line = data_in_str.find('\n', second_line) + 1
        fourth_line = data_in_str.find('\n', third_line) + 1
        #fifth_line = data_in_str.find('\n', fourth_line) + 1

        imd = data_in_str[fourth_line:] + '\n'

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



def convert_to_csv():

    driver.implicitly_wait(wait_time)
    try:
        menu = driver.find_element_by_xpath('//*[@id="stats_sh"]/div/ul/li[1]/span')  #//*[@id="stats_sh"]/div/ul/li[1]/span, //*[@id="stats_sh"]/div/ul/li[1]/span

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
    csv_btn = driver.find_element_by_xpath('//*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button')  #//*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button  //*[@id="stats_sh"]/div/ul/li[1]/div/ul/li[3]/button
    action.move_to_element(csv_btn)
    action.click().perform()
    return 0



def next_btn():
    strng = ''

    last_page = False
    f_line = True
    link_url = driver.current_url
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
        if r == 1:
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
    return strng


def execute():
    #p = read_file('dks4.csv')
    #l = player_to(p)
    #print("player_to works")
    model2 = keras.models.load_model('models\\mae2.5')

    #f = open('temp l.pickle', 'wb')
    #pickle.dump(l, f)
    #f.close()

    l = pickle.load(open('temp l.pickle', 'rb'))

    x = predict(l, model2)
    #print("predict works")
    #f = open('temp x.pickle', 'wb')
    #pickle.dump(x, f)
    #f.close()

    #load_file = open('temp x.pickle', 'rb')
    #x = pickle.load(load_file)
    #print(len(x))
    #for i in x:
        #print(i.position)
    g = algo(x)

    s = g.execute(budget=50000, n=5)
    for i in s:
        print("______Combo_______")
        for c in i:
            print(c.name, c.pp, c.cost)

if __name__ == "__main__":
    execute()




