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

loc = '中正紀念堂'

start_time = datetime.now()
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('log-level=3')

# 開啟Chrome 進入登入頁面
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://www.uber.com/tw/zh-tw/price-estimate/")

#time.sleep(2)
# 找到輸入地點的entry
entry = chrome.find_element_by_css_selector("input[placeholder='輸入上車地點']")

# Method1. 大約9秒
# 緩慢輸入 
# for w in loc:
#     entry.send_keys(w)
#     time.sleep(0.2)
    
# time.sleep(1)

# Method2. 大約8秒
entry.send_keys(loc)
time.sleep(2)

# 取得輸入起始點後的建議清單
location_list = chrome.find_elements_by_xpath('//ul[@role="listbox"]')
location_suggestions = location_list[0].text.split('\n')
end_time = datetime.now()
how_many_second = (end_time - start_time).seconds

print(location_suggestions)
print(how_many_second)
