from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import requests
import json
import time
import urllib.request
import numpy
from tkinter import messagebox 


for num_of_sample in range(14, 20):

    with open('test_data/test_sample_start_loc/test_coordinate_sample{}.txt'.format(num_of_sample), mode='r', encoding='big5') as f:
        start_loc = f.readline()
        print(start_loc)

    with open('test_data/test_sample_stop_loc/test_coordinate_sample{}.txt'.format(num_of_sample), mode='r', encoding='big5') as f:
        stop_loc = f.readline()
        print(stop_loc)


    start_time = datetime.now()

    # start_loc = '中正紀念堂, 台灣台北市中正區中山南路'
    # stop_loc =  '台灣大學, 台灣台北市大安區羅斯福路四段'
    start_choice = 0
    stop_choice = 0

    # 避免彈出視窗
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("log-level=3")

    # 開啟Chrome 進入頁面
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get("https://www.uber.com/tw/zh-tw/price-estimate/")
    time.sleep(3)

    start = chrome.find_element_by_css_selector("input[placeholder='輸入上車地點']")
    stop = chrome.find_element_by_css_selector("input[placeholder='輸入目的地']")

    # Method1. 大約39秒
    # 緩慢輸入
    # for w in start_loc:
    #     start.send_keys(w)
    #     time.sleep(0.5)

    # time.sleep(2)

    start.send_keys(start_loc)
    time.sleep(2)

    # 取得輸入起始點後的建議清單
    start_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
    start_choice_name = start_location_list[0].text.split('\n')[start_choice]

    # 指定使用者選擇的地點並點選
    current_start_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[start_choice]
    ActionChains(chrome).move_to_element(current_start_choice).click().perform()

    # 取得起始點的 cookie 和 id
    start_ck = chrome.get_cookies()
    start_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in start_ck]).encode('utf-8')
    start_id = next(c for c in start_ck if c["name"] == "_gali")['value']

    # 緩慢輸入
    # for w in stop_loc:
    #     stop.send_keys(w)
    #     time.sleep(0.5)

    # time.sleep(2)

    stop.send_keys(stop_loc)
    time.sleep(2)

    # 取得輸入終點後的建議清單
    stop_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
    stop_choice_name = stop_location_list[0].text.split('\n')[stop_choice]

    # 看使用者需要用的地址為choices裡的哪一個, 選擇建議的第一項並點選
    current_stop_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[0]
    ActionChains(chrome).move_to_element(current_stop_choice).click().perform()

    #time.sleep(3)

    # 取得點選過後的地址，為了要有正確地點給台灣大車隊用
    #correct_stop_address = stop.get_attribute('value')

    get_offer_yet = False
    while get_offer_yet != True:
        try:
            # 取得估價結果
            offers = chrome.find_elements_by_xpath('//div[@tabindex="0"]')
            offers = [o.text for o in offers if o.text.find('$') != -1]

            # 乘車方案和名稱
            uber_offer_name = offers[0].split('\n')[0]
            uber_offer_price = float(offers[0].split('\n')[1].replace('$','').replace(',',''))
            get_offer_yet = True
            prin('Success, got offer')
        except:
            print('fail to get offer')
            pass


    # 取得終點的 cookie 和 id
    stop_ck = chrome.get_cookies()
    stop_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in stop_ck]).encode('utf-8')
    stop_id = next(c for c in stop_ck if c["name"] == "_gali")['value']

    # 利用剛取得起點跟終點的cookie來抓座標軸
    uber_ck_data = {'start':[start_cookie, start_id], 'stop':[stop_cookie, stop_id]}
    uber_coordinates = {}
    uber_address_name = {}


    # 座標軸, 確切地址, 地點名稱的爬取過程
    for k, v in uber_ck_data.items():

        headers = {
                    'content-length': '101',
                    'cookie': v[0],
                    'origin': 'https://www.uber.com',
                    'referer': 'https://www.uber.com/tw/zh-tw/price-estimate/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'x-csrf-token': 'x',
                }
        payload = {
                    "type":"destination",
                    "locale":"zh-TW",
                    "id":v[1],
                    "provider":"google_places"
                   }

        url = 'https://www.uber.com/api/loadFEPlaceDetails?localeCode=zh-TW'
        res = requests.post(url, data=payload, headers= headers)

        # 紀錄座標軸 for 大都會
        lat = res.json()['data']['lat']
        lng = res.json()['data']['long']
        uber_coordinates[k] = [lng, lat]
        
        location_address = ''.join(list(reversed(res.json()['data']['addressLine2'].replace(' ','').split(','))))
        location_name = res.json()['data']['addressLine1']
        uber_address_name[k] = [location_address, location_name]

    end_time = datetime.now()
    print([uber_offer_price, uber_coordinates, start_choice_name, stop_choice_name, uber_address_name])

    how_many_second = (end_time - start_time).seconds
    print('花費時間', how_many_second)


    with open('test_data/test_sample_uber_address_name/uber_address_name_{}.txt'.format(num_of_sample), mode='w') as f:
        f.write(json.dumps(uber_address_name))

    time.sleep(5)
