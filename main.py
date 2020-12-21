import tkinter as tk
from tkinter import *
from PIL import ImageTk
from crawler import Crawler


def estimate_all(start_loc, stop_loc):

    estimate = Crawler()

    # Uber的結果
    uber_result = estimate.uber_taxi(start_loc, stop_loc)

    # 把uber回傳的資源賦值
    uber_taxi_price = uber_result[0]
    coordinates = uber_result[1]
    start_choice_name = uber_result[2]
    stop_choice_name = uber_result[3]

    # 帶入其他function中估算車資
    line_taxi_price = estimate.lin_taxi(start_loc, stop_loc, name, pwd)
    tw_taxi_price = estimate.uber_taxi(coordinates, start_choice_name, stop_choice_name)
    city_price = estimate.city(coordinates)

    return uber_taxi_price, line_taxi_price, tw_taxi_price, city_price

def start_click_searching():

    global start_entry
    global start_location_suggestions_dropdown_list

    keywords = start_entry.get()
    crawler = Crawler()
    start_location_suggestions = crawler.location_suggestions(keywords)
    try:
        start_location_suggestions_dropdown_list.destroy()
    except:
        pass
    default_variable = StringVar(window)
    default_variable.set(start_location_suggestions[0]) # default value
    start_location_suggestions_dropdown_list = OptionMenu(window, default_variable, *start_location_suggestions)
    start_location_suggestions_dropdown_list.place(x=423, y= 309)

def arrive_click_searching():

    global arrive_entry
    global arrive_location_suggestions_dropdown_list

    keywords = arrive_entry.get()
    crawler = Crawler()
    arrive_location_suggestions = crawler.location_suggestions(keywords)
    try:
        arrive_location_suggestions_dropdown_list.destroy()
    except:
        pass
    default_variable = StringVar(window)
    default_variable.set(arrive_location_suggestions[0]) # default value
    arrive_location_suggestions_dropdown_list = OptionMenu(window, default_variable, *arrive_location_suggestions)
    arrive_location_suggestions_dropdown_list.place(x=423, y= 369)

def thrifty_searching():

# 視窗頁面
window = tk.Tk()
window.title('Thrifty Cab')
window.geometry('800x600')
window.configure(bg='floral white')
window.resizable(height='False', width='False')

# 標題
lbl_title = tk.Label(text = 'Thrifty Cab', font=("Telugu MN", 100, 'bold italic'), bg='floral white')
lbl_title.place(x=110, y=150)

# 起始點
frm_start = tk.Frame(width=760, height=40, background="bisque")
frm_start.place(x=20, y=300)
lbl_start = tk.Label(text = 'Pickup Location', font = ("Telugu MN", 20), bg="bisque")
lbl_start.place(x=28, y=302)
start_entry = tk.Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
start_entry.place(x=185, y=306)
start_entry.config(highlightbackground="bisque")
search_button = Button(text='search', width=3, relief=GROOVE, command=start_click_searching)
search_button.place(x=360, y=305)
search_button.config(highlightbackground="bisque")

# 終點
frm_arrive = tk.Frame(width=760, height=40, background="bisque")
frm_arrive.place(x=20, y=360)
lbl_arrive = tk.Label(text = 'Where to?', font = ("Telugu MN", 20), bg="bisque")
lbl_arrive.place(x=50, y=362)
arrive_entry = tk.Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
arrive_entry.place(x=185, y=366)
arrive_entry.config(highlightbackground="bisque")
search_button = Button(text='search', width=3, relief=GROOVE, command=arrive_click_searching)
search_button.place(x=360, y=365)
search_button.config(highlightbackground="bisque")

# 'Thrifty' button
thrifty_btn = Button(width=10, height=1, text='Thrifty!', relief=GROOVE, font = ("Telugu MN", 20), bg='snow')
thrifty_btn.place(x=330, y=420)
thrifty_btn.config(highlightbackground='floral white')

window.mainloop()