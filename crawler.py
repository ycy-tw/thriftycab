from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import requests
import json
import time


class Crawler:

    def __init__(self):

        pass

    # 當使用者輸入地點後，透過Uber顯示的可能地點提供使用者選擇
    def location_suggestions(self, loc):

        # 避免彈出視窗
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('log-level=3')

        # 開啟Chrome 進入登入頁面
        chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
        chrome.get("https://www.uber.com/tw/zh-tw/price-estimate/")

        time.sleep(2)
        # 找到輸入地點的entry
        entry = chrome.find_element_by_css_selector("input[placeholder='輸入上車地點']")

        # 緩慢輸入
        for w in loc:
            entry.send_keys(w)
            time.sleep(1)

        # 取得輸入起始點後的建議清單
        location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
        location_suggestions = location_list[0].text.split('\n')

        return location_suggestions

    # Uber車資估算
    def uber_taxi(self, start_loc, stop_loc, start_choice=0, stop_choice=0):
    
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
        
        # 緩慢輸入
        for w in start_loc:
            start.send_keys(w)
            time.sleep(1)

        time.sleep(2)

        # 取得輸入起始點後的建議清單
        start_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
        start_choice_name = start_location_list[0].text.split('\n')[start_choice]

        # 指定使用者選擇的地點並點選
        current_start_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[start_choice]
        ActionChains(chrome).move_to_element(current_start_choice).click().perform()

        time.sleep(2)
        
        # 取得起始點的 cookie 和 id
        start_ck = chrome.get_cookies()
        start_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in start_ck]).encode('utf-8')
        start_id = next(c for c in start_ck if c["name"] == "_gali")['value']

        # 緩慢輸入
        for w in stop_loc:
            stop.send_keys(w)
            time.sleep(1)

        time.sleep(2)
        
        # 取得輸入終點後的建議清單
        stop_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
        stop_choice_name = stop_location_list[0].text.split('\n')[stop_choice]

        # 看使用者需要用的地址為choices裡的哪一個, 選擇建議的第一項並點選
        current_stop_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[0]
        ActionChains(chrome).move_to_element(current_stop_choice).click().perform()
        
        time.sleep(3)
        
        # 取得估價結果
        offers = chrome.find_elements_by_xpath('//div[@tabindex="0"]')
        offers = [o.text for o in offers if o.text.find('$') != -1]
        
        # 回傳全部乘車方案
        # uber_offers = {}
        # for i in range(len(offers)):
        #     offer_name = offers[i].split('\n')[0]
        #     offer_price = float(offers[i].split('\n')[1].replace('$','').replace(',',''))
        #     uber_offers[offer_name] = offer_price

        # 乘車方案和名稱
        uber_offer_name = offers[0].split('\n')[0]
        uber_offer_price = float(offers[0].split('\n')[1].replace('$','').replace(',',''))

        # 取得終點的 cookie 和 id
        stop_ck = chrome.get_cookies()
        stop_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in stop_ck]).encode('utf-8')
        stop_id = next(c for c in stop_ck if c["name"] == "_gali")['value']
        
        # 利用剛取得起點跟終點的cookie來抓座標軸
        uber_ck_data = {'start':[start_cookie, start_id], 'stop':[stop_cookie, stop_id]}
        uber_coordinates = {}

        # 座標軸爬取過程
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

            lat = res.json()['data']['lat']
            lng = res.json()['data']['long']
            uber_coordinates[k] = [lng, lat]
            
        return uber_offer_price, uber_coordinates, start_choice_name, stop_choice_name
    def m_taxi(self, start_loc, stop_loc, start_choice=0, stop_choice=0):
        # 避免彈出視窗
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('log-level=3')

        # 開啟Chrome 進入登入頁面
        chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
        chrome.get("https://www.uber.com/tw/zh-tw/price-estimate/")

        #time.sleep(2)
        start = chrome.find_element_by_css_selector("input[placeholder='輸入上車地點']")
        stop = chrome.find_element_by_css_selector("input[placeholder='輸入目的地']")

        # 緩慢輸入
        for w in start_loc:
            start.send_keys(w)
            time.sleep(1)

        #time.sleep(2)

        # 取得輸入起始點後的建議清單
        start_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
        choices = start_location_list[0].text.split('\n')[start_choice]

        # 選擇建議的第一項並點選
        current_start_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[start_choice]
        ActionChains(chrome).move_to_element(current_start_choice).click().perform()

        #time.sleep(2)

        '''
        為了要抓取google所提供的座標，在點完了起始點後需要先立即的get_cookie，
        取得需要的元素，等等要用requests.post來抓座標
        '''

        # 取得起始點的 cookie 和 id
        start_ck = chrome.get_cookies()
        start_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in start_ck]).encode('utf-8')
        start_id = next(c for c in start_ck if c["name"] == "_gali")['value']


        # 緩慢輸入
        for w in stop_loc:
            stop.send_keys(w)
            time.sleep(1)
            
        #time.sleep(2)

        # 取得輸入終點後的建議清單
        stop_location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
        choices = stop_location_list[0].text.split('\n')[stop_choice]

        # 看使用者需要用的地址為choices裡的哪一個, 選擇建議的第一項並點選
        current_stop_choice = chrome.find_elements_by_xpath("//*[contains(text(), '台灣')]")[stop_choice]
        ActionChains(chrome).move_to_element(current_stop_choice).click().perform()

        '''
        同樣的邏輯套用在終點的輸入上
        '''

        # 取得終點的 cookie 和 id
        stop_ck = chrome.get_cookies()
        stop_cookie = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in stop_ck]).encode('utf-8')
        stop_id = next(c for c in stop_ck if c["name"] == "_gali")['value']


        # 利用剛取得起點跟終點的cookie來抓座標軸
        uber_ck_data = {'start':[start_cookie, start_id], 'stop':[stop_cookie, stop_id]}
        uber_coordinates = {}

        # 爬取過程
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

            lat = res.json()['data']['lat']
            lng = res.json()['data']['long']
            uber_coordinates[k] = [lng, lat]


        '''
        大都會車資估算直接用資料來源抓取
        而直接從資料來源抓取要給予一些參數，也就是我們剛剛從Uber抓來的座標
        '''

        # 爬資料
        url = 'https://fare.hostar.com.tw/api/v2.0/estfare/getestfare'
        headers = {
                    'Content-Type': 'application/json, charset=UTF-8',
                   }

        payload = json.dumps({
                            "route_api":"here",
                            "waypoints":[
                                {
                                    "lng":uber_coordinates['start'][0],
                                    "lat":uber_coordinates['start'][1],
                                },
                                {
                                "lng":uber_coordinates['stop'][0],
                                 "lat":uber_coordinates['stop'][1],
                                }
                            ],
                            "app_type":"178",
                            "check_quote_fare":'true',
                            "need_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace('-','/'),
                            "check_plus_params":'false',
                            "show_debug":'false',
                            })

        res = requests.post(url, data=payload, headers=headers)

        # 結果輸出
        Metro_output = res.json()
        Metro_fare = (Metro_output['fare_info'][0]['max_fare'] +Metro_output['fare_info'][0]['min_fare']) / 2
        return Metro_fare, uber_coordinates, start_choice_name, stop_choice_name






# 取得使用者出發點選項
# 取得使用者終點選項
# 使用者確定選項後，開始計算各家價格
# 透過Uber啟動一切，Uber的下拉選單選取剛使用者選擇的上下車選項
# 大都會用Uber的座標軸來算車資
# 台灣大車隊用使用者點選的地點和座標來計算車資
# line的部份用使用者選取的結果直接輸入在上下車的位置

# Uber 的Output有 1)三個方案，2)座標軸，3)地點名稱。
# 大都會需要 座標
# 台灣大車隊需要 座標 地點名稱
# Line需要 地點名稱
