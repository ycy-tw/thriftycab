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

#line_id = 'line_email'
#line_password = 'pwd'

for num_of_sample in range(1, 13):


    with open('test_data/test_sample_start_loc/test_coordinate_sample{}.txt'.format(num_of_sample), mode='r', encoding='big5') as f:
        start_choice_name = f.readline()
        print(start_choice_name)

    with open('test_data/test_sample_stop_loc/test_coordinate_sample{}.txt'.format(num_of_sample), mode='r', encoding='big5') as f:
        stop_choice_name = f.readline()
        print(stop_choice_name)

    #line_taxi(self, start_choice_name, stop_choice_name, line_id, line_password):
    start_time = datetime.now()

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("log-level=3")

    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get("https://app.taxigo.com.tw/")

    time.sleep(3)

    Email = chrome.find_element_by_name("tid")
    Password = chrome.find_element_by_name("tpasswd")

    time.sleep(3)

    Email.send_keys(line_id)
    Password.send_keys(line_password)
    Password.submit()

    time.sleep(3)
    code_for_phone = chrome.find_element_by_class_name("mdMN06Number").text
    messagebox.showinfo("驗證碼", "請到您手機上輸入:"+str(code_for_phone))
    enter_yet = False

    while enter_yet != True:

        time.sleep(3) 

        try:
        # 登入
            Email = chrome.find_element_by_name("tid")
            Password = chrome.find_element_by_name("tpasswd")

            Email.send_keys(line_id)
            Password.send_keys(line_password)
                
            Password.submit()
            enter_yet = True

        except:
            pass

    #time.sleep(5)
    Estimate_page = False

    while Estimate_page != True:
        try:
            try:
                ad_button = chrome.find_elements_by_xpath('//button[@class="popWarning-btn h6"]')[0]
                ActionChains(chrome).move_to_element(ad_button).click().perform()
            except:
                pass

            try:
                ad_button = chrome.find_elements_by_xpath('//div[@class="notification-close-area"]')[0]
                ActionChains(chrome).move_to_element(ad_button).click().perform()
            except:
                pass

            enter_adress_button = chrome.find_elements_by_xpath('//span[@class="null"]')[0]
            ActionChains(chrome).move_to_element(enter_adress_button).click().perform()

            time.sleep(3)
            start = chrome.find_element_by_css_selector("input[placeholder='上車地點']")
            stop = chrome.find_element_by_css_selector("input[placeholder='下車地點']")
            Estimate_page = True

            print('Success')
        except:
            print('Fail to enter estimate_page')
            pass

    start_loc = start_choice_name
    stop_loc = stop_choice_name

    # 輸入上車地並點選第一個選項
    start.send_keys(start_loc)
    time.sleep(0.5)
    choice1 = chrome.find_elements_by_xpath('//div[@class="address-title-des subtitle_01"][@data-index="0"]')[1]
    ActionChains(chrome).move_to_element(choice1).click().perform()

    time.sleep(0.5)

    # 輸入下車地並點選第一個選項
    stop.send_keys(stop_loc)
    time.sleep(0.5)
    choice1 = chrome.find_elements_by_xpath('//div[@class="address-title-des subtitle_01"][@data-index="0"]')[1]
    ActionChains(chrome).move_to_element(choice1).click().perform()

    time.sleep(2)

    LINE_TAXI_PLUS = chrome.find_elements_by_xpath('//div[@class="select-car-estimate"]')[0].text
    LINE_TAXI = chrome.find_elements_by_xpath('//div[@class="select-car-estimate"]')[1].text

    index = LINE_TAXI.find('~')
    lowest = float(LINE_TAXI[:index].replace('$',''))

    end_time = datetime.now()
    cost_of_time = (end_time - start_time).seconds
    print(lowest)
    print('花了', cost_of_time)

    time.sleep(10)
