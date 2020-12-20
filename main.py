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

    keywords = start_entry.get()
    crawler = Crawler()
    Location_suggestions = crawler.location_suggestions(keywords)

    default_variable = StringVar(window)
    default_variable.set(Location_suggestions[0]) # default value
    Location_suggestions_dropdown_list = OptionMenu(window, default_variable, *Location_suggestions)
    Location_suggestions_dropdown_list.place(x=400, y= 400)


window = tk.Tk()
window.title('Thrifty Cab')
# window = iconbitmap
window.geometry('800x600')
window.resizable(height='False', width='False')

# frm_ask = tk.Frame()
# frm_ask.pack()
# lbl_ask = tk.Label(master=frm_ask, text = 'Where to?', font=("Telugu MN", 35, 'bold italic'))
# lbl_ask.pack(side=tk.TOP)

# frm_1 = tk.Frame()
# frm_1.place(x=170, y=50)
# lbl_1 = tk.Label(master=frm_1, text = 'Pickup Location', font = ("Telugu MN", 16))
# lbl_1.pack()

# ent1 = tk.Entry(width=30)
# ent1.place(x=300, y=50)
# # start = entry.get()
# # entry.delete(0, tk.END)

# frm_2 = tk.Frame()
# frm_2.place(x=200, y=80)
# lbl_2 = tk.Label(master=frm_2, text = 'Where to?', font = ('Telugu MN', 16))
# lbl_2.pack()

# ent2 = tk.Entry(width=30)
# ent2.place(x=300, y=80)

start_entry = tk.Entry(bg="gray", relief=GROOVE, width=20)#,textvariable=v
start_entry.place(x=300, y=300)

search_button = Button(text='搜尋', width=8, relief=GROOVE, command=start_click_searching)
search_button.place(x=400, y=300)


window.mainloop()