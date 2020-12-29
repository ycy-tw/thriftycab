from tkinter import *
from crawler import Crawler
from PIL import ImageTk,Image
#from view import * #選單欄對應的各個子頁面

class MainPage():

    def __init__(self, master=None, mail=None, pwd=None):

        self.root = master #定義內部變數root
        self.root.geometry('800x600') #設定視窗大小
        #self.root.configure(bg='floral white')
        self.root.image1 = Image.open("bg2.jpg")
        self.root.test = ImageTk.PhotoImage(self.root.image1)
        self.root.label1 = Label(image=self.root.test)
        self.root.label1.image = self.root.test
        self.root.label1.pack()
        self.root.resizable(height='False', width='False')

        self.mail = mail
        self.pwd = pwd
        self.CreatePage()

    def start_click_searching(self):

        # global start_entry
        # global start_location_suggestions_dropdown_list
        # global start_default_variable

        keywords = self.start_entry.get()
        crawler = Crawler()
        start_location_suggestions = crawler.location_suggestions(keywords)

        try:
            self.start_location_suggestions_dropdown_list.destroy()
        except:
            pass

        self.start_default_variable = StringVar(self.root)
        self.start_default_variable.set(start_location_suggestions[0]) # default value
        self.start_location_suggestions_dropdown_list = OptionMenu(self.root, self.start_default_variable, *start_location_suggestions)
        self.start_location_suggestions_dropdown_list.config(width=34)
        self.start_location_suggestions_dropdown_list.place(x=97, y= 265)


    def arrive_click_searching(self):

        # global arrive_entry
        # global arrive_location_suggestions_dropdown_list
        # global arrive_default_variable

        keywords = self.arrive_entry.get()
        crawler = Crawler()
        arrive_location_suggestions = crawler.location_suggestions(keywords)

        try:
            self.arrive_location_suggestions_dropdown_list.destroy()
        except:
            pass

        self.arrive_default_variable = StringVar(self.root)
        self.arrive_default_variable.set(arrive_location_suggestions[0]) # default value
        self.arrive_location_suggestions_dropdown_list = OptionMenu(self.root, self.arrive_default_variable, *arrive_location_suggestions)
        self.arrive_location_suggestions_dropdown_list.config(width=34)
        self.arrive_location_suggestions_dropdown_list.place(x=97, y= 365)


    def thrifty_searching(self, start_loc=None, stop_loc=None):

        start_loc = self.start_default_variable.get()
        stop_loc = self.arrive_default_variable.get()

        mail = self.mail
        pwd = self.pwd

        estimate = Crawler()

        # Uber的結果
        uber_result = estimate.uber_taxi(start_loc, stop_loc)

        # 把uber回傳的資源賦值
        uber_taxi_price = uber_result[0]
        coordinates = uber_result[1]
        start_choice_name = uber_result[2]
        stop_choice_name = uber_result[3]
        uber_address_name = uber_result[4]

        print('uebr成功', uber_taxi_price)

        # 如果使用者沒輸入email的話，代表不使用line taxi車資估算
        if mail is None:

            line_taxi_price = 0
            print('使用者不用line', line_taxi_price)

        else:
            line_taxi_price = estimate.line_taxi(start_loc, stop_loc, mail, pwd)
            print('line成功', line_taxi_price)

        # 帶入其他function中估算車資
        tw_taxi_price = estimate.tw_taxi(uber_address_name)
        print('tw成功', tw_taxi_price)

        city_price = estimate.m_taxi(coordinates)
        print('city成功', city_price)

        firm_list = ['Uber', 'LINE TAXI', '台灣大車隊', '大都會計程車']
        price_list = [uber_taxi_price, line_taxi_price, tw_taxi_price, city_price]

        result = []
        for i in range(4):
            result.append((firm_list[i], price_list[i]))

        # 把結果由小到大排序
        result = sorted(list(result), key=lambda x: (x[1]))

        # 建立一塊區域呈現結果
        self.result_frame = Frame(self.root, bg='white')
        self.result_frame.place(x=490, y=258)

        # 把沒結果(結果為0)的估計車資改成無估計車資
        for i in range(len(result)):

            firm = result[i][0]
            fare = result[i][1]
            check_fare = fare

            if fare == 0:
                check_fare = '無估計車資'
            else:
                check_fare = str('NT$ ')+str(check_fare)

            # 由小到大呈現在畫面上
            self.firm_name = Label(self.result_frame, text=firm, font = ("Telugu MN", 18), bg="white")
            self.firm_name.grid(row=i, column=0)

            self.estimate_price = Label(self.result_frame, text=check_fare, font = ("Telugu MN", 18), bg="white")
            self.estimate_price.grid(row=i, column=1)


    def Reset(self):

        self.start_entry.delete(0, END)
        self.arrive_entry.delete(0, END)
        self.start_location_suggestions_dropdown_list.destroy()
        self.arrive_location_suggestions_dropdown_list.destroy()
        self.result_frame.destroy()
        #self.estimate_price.destroy()

    def CreatePage(self):

        # 標題
        self.lbl_title = Label(text = 'Thrifty Cab', font=("Telugu MN", 60, 'bold italic'), bg='white')
        self.lbl_title.place(x=220, y=110)

        # 起始點
        self.frm_start = Frame(width=403, height=40, background="lemon chiffon")
        self.frm_start.place(x=50, y=210)
        self.frm_startbox = Frame(width=30, height=30, background="lemon chiffon")
        self.frm_startbox.place(x=55, y=263)
        self.frm_startlist = Frame(width=363, height=40, background="gray98", relief='solid', borderwidth=1)
        self.frm_startlist.place(x=90, y=260)
        self.lbl_start = Label(text = 'Pickup Location', font = ("Telugu MN", 20), bg="lemon chiffon")
        self.lbl_start.place(x=58, y=212)
        self.start_entry = Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
        self.start_entry.place(x=215, y=216)
        self.start_entry.config(highlightbackground="lemon chiffon")
        self.search_button = Button(text='search', width=3, relief=GROOVE, command=self.start_click_searching)
        self.search_button.place(x=390, y=215)
        self.search_button.config(highlightbackground="lemon chiffon")

        # 終點
        self.frm_arrive = Frame(width=403, height=40, background="bisque")
        self.frm_arrive.place(x=50, y=310)
        self.frm_arrivelist = Frame(width=363, height=40, background="gray98", relief='solid', borderwidth=1)
        self.frm_arrivelist.place(x=90, y=360)
        self.frm_arrivebox = Frame(width=30, height=30, background="bisque")
        self.frm_arrivebox.place(x=55, y=363)
        self.lbl_arrive = Label(text = 'Where to?', font = ("Telugu MN", 20), bg="bisque")
        self.lbl_arrive.place(x=58, y=312)
        self.arrive_entry = Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
        self.arrive_entry.place(x=215, y=316)
        self.arrive_entry.config(highlightbackground="bisque")
        self.search_button = Button(text='search', width=3, relief=GROOVE, command=self.arrive_click_searching)
        self.search_button.place(x=390, y=315)
        self.search_button.config(highlightbackground="bisque")

        # 'Thrifty' button
        self.thrifty_btn = Button(width=10, height=1, text='Thrifty!', relief=GROOVE, font = ("Telugu MN", 20), bg='snow', command=self.thrifty_searching)
        self.thrifty_btn.place(x=170, y=420)
        self.thrifty_btn.config(highlightbackground='white')

        # 'Result' board
        self.frm_result = Frame(width=263, height=187, background="white",relief='solid', borderwidth=2)
        self.frm_result.place(x=473, y=212)
        self.frm_result1 = Frame(width=263, height=35, background="white",relief='solid', borderwidth=2)
        self.frm_result1.place(x=473, y=212)
        self.lbl_result = Label(text = 'Result', font = ("Telugu MN", 15), bg="white")
        self.lbl_result.place(x=578, y=215)

        # 'Reset' button
        self.reset_btn = Button(width=10, height=1, text='Reset', relief=GROOVE, font = ("Telugu MN", 20), bg='snow', command=self.Reset)
        self.reset_btn.place(x=530, y=420)
        self.reset_btn.config(highlightbackground='white')


    #self.testvar = Label(text = 'Email:'+ self.mail).grid(row=1, stick=W, pady=10)



    
  