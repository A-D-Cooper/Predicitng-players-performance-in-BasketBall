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


wait_time = 30

driver = webdriver.Chrome("C:/SeleniumDrivers/chromedriver.exe")


def login():
    username = ####
    password = ####
    driver.get("https://stathead.com/users/login.cgi")
    driver.implicitly_wait(30)

    usernm_txt = driver.find_element_by_id("username")
    pas_txt = driver.find_element_by_id("password")

    usernm_txt.send_keys(username)
    pas_txt.send_keys(password)

    sub_btn = driver.find_element_by_id("sh-login-button")
    sub_btn.click()


def convert_to_csv():
    #driver.get("https://stathead.com/football/pgl_finder.cgi")
    #driver.implicitly_wait(30)

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

        pre_file.write(imd)

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

        pre_file.write(imd)

        concat_str = strng + data_in_str[fifth_line:] + '\n'

        #print(data_in_str[fifth_line:])
        #print(first_line, second_line, third_line, fourth_line, fifth_line, sixth_line)

    return concat_str


def str_concat2(strng, f_line):

    driver.implicitly_wait(wait_time)

    data_in_str = driver.find_element_by_xpath('//*[@id="csv_stats"]').text  #//*[@id="csv_stats"]/text()[2]  //*[@id="csv_stats"]/text()[2]

    if f_line:
        first_line = data_in_str.find('\n') + 1
        second_line = data_in_str.find('\n', first_line) + 1
        third_line = data_in_str.find('\n', second_line) + 1
        fourth_line = data_in_str.find('\n', third_line) + 1
        fifth_line = data_in_str.find('\n', fourth_line) + 1

        imd = data_in_str[fifth_line:] + '\n'

        pre_file.write(imd)

        concat_str = strng + imd

        #print(data_in_str[fourth_line:])


        #print(first_line, second_line, third_line, fourth_line, fifth_line)

    else:
        first_line = data_in_str.find('\n') + 1
        second_line = data_in_str.find('\n', first_line) + 1
        third_line = data_in_str.find('\n', second_line) + 1
        fourth_line = data_in_str.find('\n', third_line) + 1
        fifth_line = data_in_str.find('\n', fourth_line) + 1
        sixth_line = data_in_str.find('\n', fifth_line) + 1

        imd = data_in_str[sixth_line:] + '\n'

        pre_file.write(imd)

        concat_str = strng + imd

        #print(data_in_str[sixth_line:])
        #print(first_line, second_line, third_line, fourth_line, fifth_line, sixth_line)

    return concat_str


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

        if i==1:
            strng = str_concat(strng, f_line)
        else:
            strng = str_concat2(strng, f_line)

        f_line = False

        soup = BeautifulSoup(html_source, 'lxml')
        links = soup.find_all('div', class_='prevnext')

        for link in links:
            l = link.find_all('a', class_='button2 next')
            if len(l) == 0:
                last_page = True
            else:
                link_url = "https://stathead.com" + l[0]['href']
    pre_file.close()
    return strng


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
    pre_file = open('pre file.csv', 'a', encoding='utf-8')
    login()
    write_to_csv()
    pre_file.close()
