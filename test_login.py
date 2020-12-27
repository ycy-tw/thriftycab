from tkinter import *
from tkinter.messagebox import *
from test_mainpage import *


class LoginPage:

    def __init__(self, master=None):

        self.root = master #定義內部變數root
        self.root.geometry('%dx%d' % (400, 300)) #設定視窗大小
        self.root.configure(bg='floral white')
        self.root.resizable(height='False', width='False')

        self.username = StringVar()
        self.password = StringVar()
        self.createPage()
          
    def createPage(self):

        self.page = Frame(self.root) #建立Frame
        self.page.pack()

        Label(self.page, text = 'LINE SERVICE ACTIVATE').grid(row=0, stick=W)
        Label(self.page, text = 'Email: ').grid(row=1, stick=W, pady=15)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text = 'Password: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)

        Button(self.page, text='Activate', command=self.use_line_service).grid(row=3, stick=W, pady=10)
        Button(self.page, text='Skip', command=self.skip_line_service).grid(row=3, column=1, stick=E)

    def use_line_service(self):

        self.mail = self.username.get()
        self.pwd = self.password.get()

        self.page.destroy()
        MainPage(self.root, self.mail, self.pwd)  

    def skip_line_service(self):

        self.page.destroy()
        MainPage(self.root)

