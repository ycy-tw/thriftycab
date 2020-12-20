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
    Location_suggestions_dropdown_list.place(x=495, y= 309)

def arrive_click_searching():

    global start_entry

    keywords = arrive_entry.get()
    crawler = Crawler()
    Location_suggestions = crawler.location_suggestions(keywords)

    default_variable = StringVar(window)
    default_variable.set(Location_suggestions[0]) # default value
    Location_suggestions_dropdown_list = OptionMenu(window, default_variable, *Location_suggestions)
    Location_suggestions_dropdown_list.place(x=495, y= 369)


window = tk.Tk()
window.title('Thrifty Cab')
# window = iconbitmap
window.geometry('800x600')
window.configure(bg='floral white')
window.resizable(height='False', width='False')

lbl_title = tk.Label(text = 'Thrifty Cab', font=("Telugu MN", 100, 'bold italic'), bg='floral white')
lbl_title.place(x=110, y=150)

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
clear_button = Button(text='clear', width=3, relief=GROOVE) #command=
clear_button.place(x=423, y=305)
clear_button.config(highlightbackground="bisque")

frm_arrive = tk.Frame(width=760, height=40, background="bisque")
frm_arrive.place(x=20, y=360)
lbl_arrive = tk.Label(text = 'Where to?', font = ("Telugu MN", 20), bg="bisque")
lbl_arrive.place(x=50, y=362)
arrive_entry = tk.Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
arrive_entry.place(x=185, y=366)
arrive_entry.config(highlightbackground="bisque")
search_button = Button(text='search', width=3, relief=RAISED, command=arrive_click_searching)
search_button.place(x=360, y=365)
search_button.config(highlightbackground="bisque")
clear_button = Button(text='clear', width=3, relief=GROOVE) #command=
clear_button.place(x=423, y=365)
clear_button.config(highlightbackground="bisque")

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




window.mainloop()