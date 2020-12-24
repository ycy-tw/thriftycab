from tkinter import *
from crawler import Crawler
#from view import * #選單欄對應的各個子頁面

class MainPage():

    def __init__(self, master=None, mail=None, pwd=None):

        self.root = master #定義內部變數root
        self.root.geometry('1000x750') #設定視窗大小
        self.root.configure(bg='floral white')
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
        start_location_suggestions_dropdown_list = OptionMenu(self.root, self.start_default_variable, *start_location_suggestions)
        start_location_suggestions_dropdown_list.place(x=423, y= 309)


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
        arrive_location_suggestions_dropdown_list = OptionMenu(self.root, self.arrive_default_variable, *arrive_location_suggestions)
        arrive_location_suggestions_dropdown_list.place(x=423, y= 369)


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

        # 帶入其他function中估算車資
        tw_taxi_price = estimate.tw_taxi(uber_address_name)
        print('tw成功', tw_taxi_price)

        city_price = estimate.m_taxi(coordinates)
        print('city成功', city_price)

        line_taxi_price = estimate.line_taxi(start_loc, stop_loc, mail, pwd)
        print('line成功', line_taxi_price)

        firm_list = ['Uber', 'LINE', 'TW', 'Metro']
        price_list = [uber_taxi_price, line_taxi_price, tw_taxi_price, city_price]

        result = []
        for i in range(4):
            result.append((firm_list[i], price_list[i]))

        # 把結果由小到大排序
        result = sorted(list(result), key=lambda x: (x[1]))

        for i in range(len(result)):

            # 由小到大呈現在畫面上
            self.firm_name = Label(text=result[i][0], font = ("Telugu MN", 20), bg="bisque")
            self.firm_name.place(x= 100, y= 400  + i*20)

            self.estimate_price = Label(text=result[i][1], font = ("Telugu MN", 20), bg="bisque")
            self.estimate_price.place(x= 120, y= 400  + i*20)


    def CreatePage(self):

        # 標題
        self.lbl_title = Label(text = 'Thrifty Cab', font=("Telugu MN", 100, 'bold italic'), bg='floral white')
        self.lbl_title.place(x=110, y=150)

        # 起始點
        self.frm_start = Frame(width=760, height=40, background="bisque")
        self.frm_start.place(x=20, y=300)
        self.lbl_start = Label(text = 'Pickup Location', font = ("Telugu MN", 20), bg="bisque")
        self.lbl_start.place(x=28, y=302)
        self.start_entry = Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
        self.start_entry.place(x=185, y=306)
        self.start_entry.config(highlightbackground="bisque")
        self.search_button = Button(text='search', width=3, relief=GROOVE, command=self.start_click_searching)
        self.search_button.place(x=360, y=305)
        self.search_button.config(highlightbackground="bisque")

        # 終點
        self.frm_arrive = Frame(width=760, height=40, background="bisque")
        self.frm_arrive.place(x=20, y=360)
        self.lbl_arrive = Label(text = 'Where to?', font = ("Telugu MN", 20), bg="bisque")
        self.lbl_arrive.place(x=50, y=362)
        self.arrive_entry = Entry(bg="gray88", relief=GROOVE, width=18,)#,textvariable=v
        self.arrive_entry.place(x=185, y=366)
        self.arrive_entry.config(highlightbackground="bisque")
        self.search_button = Button(text='search', width=3, relief=GROOVE, command=self.arrive_click_searching)
        self.search_button.place(x=360, y=365)
        self.search_button.config(highlightbackground="bisque")

        # 'Thrifty' button
        self.thrifty_btn = Button(width=10, height=1, text='Thrifty!', relief=GROOVE, font = ("Telugu MN", 20), bg='snow', command=self.thrifty_searching)
        self.thrifty_btn.place(x=330, y=420)
        self.thrifty_btn.config(highlightbackground='floral white')


    #self.testvar = Label(text = 'Email:'+ self.mail).grid(row=1, stick=W, pady=10)



    
   # def createPage(self):
   #  self.inputPage = InputFrame(self.root) # 建立不同Frame
   #  self.queryPage = QueryFrame(self.root)
   #  self.countPage = CountFrame(self.root)
   #  self.aboutPage = AboutFrame(self.root)
   #  self.inputPage.pack() #預設顯示資料錄入介面
   #  menubar = Menu(self.root)
   #  menubar.add_command(label='資料錄入', command = self.inputData)
   #  menubar.add_command(label='查詢', command = self.queryData)
   #  menubar.add_command(label='統計', command = self.countData)
   #  menubar.add_command(label='關於', command = self.aboutDisp)
   #  self.root['menu'] = menubar # 設定選單欄
    
   # def inputData(self):
   #  self.inputPage.pack()
   #  self.queryPage.pack_forget()
   #  self.countPage.pack_forget()
   #  self.aboutPage.pack_forget()
    
   # def queryData(self):
   #  self.inputPage.pack_forget()
   #  self.queryPage.pack()
   #  self.countPage.pack_forget()
   #  self.aboutPage.pack_forget()
    
   # def countData(self):
   #  self.inputPage.pack_forget()
   #  self.queryPage.pack_forget()
   #  self.countPage.pack()
   #  self.aboutPage.pack_forget()
    
   # def aboutDisp(self):
   #  self.inputPage.pack_forget()
   #  self.queryPage.pack_forget()
   #  self.countPage.pack_forget()
   #  self.aboutPage.pack()