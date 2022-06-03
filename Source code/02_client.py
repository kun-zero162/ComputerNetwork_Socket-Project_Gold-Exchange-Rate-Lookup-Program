from os import lseek
import socket
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import Tk, Canvas, Frame, BOTH, NW
from tkinter import *
from datetime import datetime

from PIL import Image, ImageTk
import PIL.Image
import PIL.ImageTk

from ctypes import FormatError
from typing import Counter
import socket
import threading
import pyodbc


import json
import requests

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
DISCONNECT = "x"

# define sever name and database name
SERVER_NAME = "DESKTOP-T8AA3QI"
DATABASE_NAME = "Socket_MMT"

# option
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
DELETE = "delete"
GETDOJIDATA = "getdojidata"
GETSJCDATA = "getsjcdata"
GETPNJDATA = "getpnjdata"

# Gui-app


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Account")
        self.geometry("350x450")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.configure(bg="red")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage, SigupPage, Connect_Server_Page):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.showPage(Connect_Server_Page)

    def showPage(self, container):
        frame = self.frames[container]
        if container == StartPage:
            self.geometry("600x400")
        elif container == HomePage:
            self.geometry("600x400")
        elif container == SigupPage:
            self.geometry("400x500")
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = LOGOUT
                client.sendall(option.encode(FORMAT))
            except:
                pass

    def Connect_to_server(self, curFrame, sck):
        IP = curFrame.entry.get()
        if IP == "":
            curFrame.label_notice["text"] = "IP cannot be empty"
            return
        elif IP == HOST:
            self.showPage(StartPage)
        elif IP != HOST:
            curFrame.label_notice["text"] = "Invalid address"
            return

    def Login(self, curFrame, sck):
        try:
            username = curFrame.entry_username.get()
            password = curFrame.entry_password.get()

            if username == "" or password == "":
                curFrame.label_notice["text"] = "Username or password cannot be empty"
                return
            # notice server for starting log in
            option = LOGIN
            sck.sendall(option.encode(FORMAT))

            # send username and password to server
            sck.sendall(username.encode(FORMAT))
            print("input:", username)

            sck.recv(1024)
            print("s responded")

            sck.sendall(password.encode(FORMAT))
            print("input:", password)

            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)

            if accepted == "1":
                messagebox.showerror(title="ERROR", message="ADMIN")
                curFrame.label_notice["text"] = ""
            elif accepted == "2":
                self.showPage(HomePage)
            elif accepted == "3":
                curFrame.label_notice["text"] = "Invalid password and username!"
            elif accepted == "0":
                curFrame.label_notice["text"] = "Username already logged in"
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")
            sck.close()

    def signUp(self, curFrame, sck):
        try:
            username = curFrame.entry_username.get()
            password = curFrame.entry_password.get()

            if username == "" or password == "":
                curFrame.label_notice["text"] = "Username or password cannot be empty"
                return
            # notice server for starting log in
            option = SIGNUP
            sck.sendall(option.encode(FORMAT))

            # send username and password to server
            sck.sendall(username.encode(FORMAT))
            print("Input:", username)

            sck.recv(1024)
            print("s responded")

            sck.sendall(password.encode(FORMAT))
            print("Input:", password)

            # see if login is accepted
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)

            if accepted == "True":
                self.showPage(StartPage)
            else:
                curFrame.label_notice["text"] = "username already exists"

        except:
            curFrame.label_notice["text"] = "Error 404: Server is not responding"
            print("404")


    def logout(self, curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)

            if accepted == "True":
                self.showPage(StartPage)
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("404")

    def getDOJIData(self, curFrame, sck):
        try:
            option = GETDOJIDATA
            sck.sendall(option.encode(FORMAT))

            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)
            return accepted
        except:
            print("No data")
            sck.close()
    def getSJCData(self, curFrame, sck):
        try:
            option = GETSJCDATA
            sck.sendall(option.encode(FORMAT))

            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)
            return accepted
        except:
            print("No data")
            sck.close()
    def getPNJData(self, curFrame, sck):
        try:
            option = GETPNJDATA
            sck.sendall(option.encode(FORMAT))

            accepted = sck.recv(1024).decode(FORMAT)
            print("accepted: " + accepted)
            return accepted
        except:
            print("No data")
            sck.close()

# Trang dang nhap or dang ky


class StartPage(tk.Frame):
    def __init__(self, parent, Controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='whitesmoke')

        img = PIL.Image.open("covid.png")
        img = img.resize((300, 400))
        photo = PIL.ImageTk.PhotoImage(img)

        label = Label(self, image=photo)
        label.image = photo  # keep a reference!
        label.place(x=0, y=0)

        imgLogo = PIL.Image.open("Logo.png")
        imgLogo = imgLogo.resize((100, 100))
        photoLogo = PIL.ImageTk.PhotoImage(imgLogo)

        labelLogo = Label(self, image=photoLogo)
        labelLogo.image = photoLogo  # keep a reference!
        labelLogo.place(x=405, y=15)

        label_title = tk.Label(self, text="LOGIN FOR CLIENT", bg='whitesmoke', fg="red", font=(
            "times new roman", 17, "bold"))
        label_username = tk.Label(self, text="Tài khoản", bg='whitesmoke', fg="green", font=(
            "times new roman", 13, "bold"))
        label_password = tk.Label(self, text="Mật khẩu", bg='whitesmoke', fg="green", font=(
            "times new roman", 13, "bold"))

        self.label_notice = tk.Label(self, text="", bg="bisque2", fg='red')
        self.entry_username = tk.Entry(self, width=20)
        self.entry_password = tk.Entry(self, width=20)

        button_SignIn = tk.Button(self, text="Đăng nhập", bg='dodgerblue', fg="white", font=(
            "times new roman", 10, "bold"), command=lambda: Controller.Login(self, client))
        button_SignIn.configure(width=10)

        button_SignUp = tk.Button(self, text="Bạn chưa có tài khoản?", bg='dodgerblue', fg="white", font=("times new roman", 10, "bold"), command=lambda: Controller.showPage(SigupPage))
        button_SignUp.configure(width=20)

        label_title.place(x=335, y=110)
        label_username.place(x=413, y=160)
        self.entry_username.place(x=390, y=185)

        label_password.place(x=413, y=215)
        self.entry_password.place(x=390, y=240)

        self.label_notice.place(x=350, y=270)

        button_SignIn.place(x=413, y=300)
        button_SignUp.place(x=380, y=330)


class Connect_Server_Page(tk.Frame):
    def __init__(self, parent, Controller):
        tk.Frame.__init__(self, parent)
        imgLogo = PIL.Image.open("Logo.png")
        imgLogo = imgLogo.resize((130, 130))
        photoLogo = PIL.ImageTk.PhotoImage(imgLogo)

        labelLogo = Label(self, image=photoLogo)
        labelLogo.image = photoLogo  # keep a reference!
        labelLogo.place(x=110, y=15)

        label_title = tk.Label(self, text="CONNECT TO SERVER", bg='whitesmoke', fg="red", font=(
            "times new roman", 16, "bold"))
        label_title.place(x=60, y=150)

        label_text = tk.Label(self, text="Enter IP address Server", bg='whitesmoke', font=("times new roman", 12))
        label_text.place(x=100, y=230)

        self.entry = tk.Entry(self, width=25)
        self.entry.place(x=100, y=260)

        self.label_notice = tk.Label(self, text="", bg="bisque2", fg='red')
        self.label_notice.place(x=120, y=290)

        button = tk.Button(self, text="CONNECT", bg='dodgerblue', fg="white", font=(
            "times new roman", 10, "bold"), command=lambda: Controller.Connect_to_server(self, client))
        button.configure(width=10)
        button.place(x=135, y=350)

# Trang hiển thị thông tin cần tìm kiếm


class HomePage(tk.Frame):
    def __init__(self, parent, Controller):
        tk.Frame.__init__(self, parent)
    
        frame1 = tk.Frame(self)
        label_title = tk.Label(frame1, text="TỶ GIÁ VÀNG VIỆT NAM", fg="red", font=("arial", 20, "bold"))
        label_title.pack()
        frame1.pack()

        frame2 = tk.Frame(self)
        label = tk.Label(frame2, text="Option:", font=("arial", 13))
        label.grid(column=0, row=1, pady=20)

        list = ["All", "DOJI", "SJC", "PNJ","DOJI Can Tho", "DOJI Da Nang", "DOJI HCM", "DOJI Ha Noi", "SJC HCM", "SJC Ha Noi", "SJC Nhan 99.99%", "SJC Trang suc 99.99%", "PNJ Nhan 24K", "PNJ Nu trang 10K", "PNJ Nu trang 14K", "PNJ Nu trang 18K", "PNJ Nu trang 24K"]
        Combo = ttk.Combobox(frame2, values=list)
        Combo.set("Pick an Gold")
        Combo.grid(column=1, row=1, padx=5, pady=5)
        calendar = DateEntry(frame2, width=20, year=2021)
        calendar.grid(column=2, row=1)

        self.label_notice2 = tk.Label(frame2, text="")
        self.label_notice2.grid(column=3, row=1)

        frame4 = tk.Frame(self)
        search = tk.Button(frame2, text="Search", bg='cornflowerblue', command=lambda: self.drawTree(parent, Controller, frame4, Combo))
        search.grid(column=4, row=1)

        frame2.pack()

        frame3 = tk.Frame(self)

        btn_logout = tk.Button(frame3, text="Log out", command=lambda: Controller.logout(self, client))
        btn_logout.pack()
        

        style = ttk.Style(self)

        style.configure("mystyle.Treeview", background="#fdde54", highlightthickness=1, bd=1, font=('Times New Roman', 12))  # Modify the font of the body
        # Modify the font of the headings
        style.configure("mystyle.Treeview.Heading")
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', { 'sticky': 'nswe'})])  # Remove the borders
        columns = ("Name", "Buy price", "Sell price")
        self.table = ttk.Treeview(self, style="mystyle.Treeview", selectmode='browse', columns=columns, show='headings')
        self.table.heading("Name", text="Name", anchor=tk.CENTER)
        self.table.heading("Buy price", text="Buy price", anchor=tk.CENTER)
        self.table.heading("Sell price", text="Sell price", anchor=tk.CENTER)
        self.table.pack()
        frame3.pack()

    def drawTree(self, parent, appController, frame4, Combo):
        tk.Frame.__init__(self, parent)

        # Lấy dữ liệu ở dạng chuỗi
        data1 = appController.getDOJIData(self, client)
        data_json1 = json.loads(data1)  # ta chuyển chuỗi sang object json
        result1 = data_json1['results']

        # Lấy dữ liệu ở dạng chuỗi
        data2 = appController.getSJCData(self, client)
        data_json2 = json.loads(data2)  # ta chuyển chuỗi sang object json
        result2 = data_json2['results']

        # Lấy dữ liệu ở dạng chuỗi
        data3 = appController.getPNJData(self, client)
        data_json3 = json.loads(data3)  # ta chuyển chuỗi sang object json
        result3 = data_json3['results']

        choice = Combo.get()
        print(choice)
        if choice == "Pick an Gold":
            return

        elif choice == "All":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI Can Tho", values=(
                    "DOJI Can Tho", i['buy_ct'], i['sell_ct']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI Da Nang", values=(
                    "DOJI Da Nang", i['buy_dn'], i['sell_dn']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI HCM", values=(
                    "DOJI HCM", i['buy_hcm'], i['sell_hcm']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI Ha Noi", values=(
                    "DOJI Ha Noi", i['buy_hn'], i['sell_hn']))
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SCJ HCM", values=(
                    "SCJ HCM", i['buy_1c'], i['sell_1c']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Ha Noi", values=(
                    "SCJ Ha Noi", i['buy_1l'], i['sell_1l']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Nhan 99.99%", values=(
                    "SCJ Nhan 99.99%", i['buy_nhan1c'], i['sell_nhan1c']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Trang suc 99.99%", values=(
                    "SCJ Trang suc 99.99%", i['buy_trangsuc49'], i['sell_trangsuc49']))
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nhan 24K", values=(
                    "PNJ Nhan 24K", i['buy_nhan_24k'], i['sell_nhan_24k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 10K", values=(
                    "PNJ Nu trang 10K", i['buy_nt_10k'], i['sell_nt_10k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 14K", values=(
                    "PNJ Nu trang 14K", i['buy_nt_14k'], i['sell_nt_14k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 18K", values=(
                    "PNJ Nu trang 18K", i['buy_nt_18k'], i['sell_nt_18k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 24K", values=(
                    "PNJ Nu trang 24K", i['buy_nt_24k'], i['sell_nt_24k']))
            self.table.pack(pady=20)

        elif choice == "DOJI":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI Can Tho", values=(
                    "DOJI Can Tho", i['buy_ct'], i['sell_ct']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI Da Nang", values=(
                    "DOJI Da Nang", i['buy_dn'], i['sell_dn']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI HCM", values=(
                    "DOJI HCM", i['buy_hcm'], i['sell_hcm']))
                self.table.insert(parent='', index='end', iid=None, text="DOJI Ha Noi", values=(
                    "DOJI Ha Noi", i['buy_hn'], i['sell_hn']))
            self.table.pack(pady=20)

        elif choice == "SJC":
            self.table.delete(*self.table.get_children())
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SCJ HCM", values=(
                    "SCJ HCM", i['buy_1c'], i['sell_1c']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Ha Noi", values=(
                    "SCJ Ha Noi", i['buy_1l'], i['sell_1l']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Nhan 99.99%", values=(
                    "SCJ Nhan 99.99%", i['buy_nhan1c'], i['sell_nhan1c']))
                self.table.insert(parent='', index='end', iid=None, text="SCJ Trang suc 99.99%", values=(
                    "SCJ Trang suc 99.99%", i['buy_trangsuc49'], i['sell_trangsuc49']))
            self.table.pack(pady=20)

        elif choice == "PNJ":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nhan 24K", values=(
                    "PNJ Nhan 24K", i['buy_nhan_24k'], i['sell_nhan_24k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 10K", values=(
                    "PNJ Nu trang 10K", i['buy_nt_10k'], i['sell_nt_10k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 14K", values=(
                    "PNJ Nu trang 14K", i['buy_nt_14k'], i['sell_nt_14k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 18K", values=(
                    "PNJ Nu trang 18K", i['buy_nt_18k'], i['sell_nt_18k']))
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 24K", values=(
                    "PNJ Nu trang 24K", i['buy_nt_24k'], i['sell_nt_24k']))
            self.table.pack(pady=20)

        elif choice == "DOJI Can Tho":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI Can Tho", values=(
                    "DOJI Can Tho", i['buy_ct'], i['sell_ct']))
            self.table.pack(pady=20)
        elif choice == "DOJI Da Nang":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI Da Nang", values=(
                    "DOJI Da Nang", i['buy_dn'], i['sell_dn']))
            self.table.pack(pady=20)
        elif choice == "DOJI HCM":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI HCM", values=(
                    "DOJI HCM", i['buy_hcm'], i['sell_hcm']))
            self.table.pack(pady=20)
        elif choice == "DOJI Ha Noi":
            self.table.delete(*self.table.get_children())
            for i in result1:
                self.table.insert(parent='', index='end', iid=None, text="DOJI Ha Noi", values=(
                    "DOJI Ha Noi", i['buy_hn'], i['sell_hn']))
            self.table.pack(pady=20)

        elif choice == "SJC HCM":
            self.table.delete(*self.table.get_children())
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SJC HCM", values=(
                    "SJC HCM", i['buy_1c'], i['sell_1c']))
            self.table.pack(pady=20)
        elif choice == "SJC Ha Noi":
            self.table.delete(*self.table.get_children())
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SJC Ha Noi", values=(
                    "SJC Ha Noi", i['buy_1l'], i['sell_1l']))
            self.table.pack(pady=20)
        elif choice == "SJC Nhan 99.99%":
            self.table.delete(*self.table.get_children())
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SJC Nhan 99.99%", values=(
                    "SJC Nhan 99.99%", i['buy_nhan1c'], i['sell_nhan1c']))
            self.table.pack(pady=20)
        elif choice == "SJC Trang suc 99.99%":
            self.table.delete(*self.table.get_children())
            for i in result2:
                self.table.insert(parent='', index='end', iid=None, text="SJC Trang suc 99.99%", values=(
                    "SJC Trang suc 99.99%", i['buy_trangsuc49'], i['sell_trangsuc49']))
            self.table.pack(pady=20)

        elif choice == "PNJ Nhan 24K":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nhan 24K", values=(
                    "PNJ Nhan 24K", i['buy_nhan_24k'], i['sell_nhan_24k']))
            self.table.pack(pady=20)
        elif choice == "PNJ Nu trang 10K":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 10K", values=(
                    "PNJ Nu trang 10K", i['buy_nt_10k'], i['sell_nt_10k']))
            self.table.pack(pady=20)
        elif choice == "PNJ Nu trang 14K":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 14K", values=(
                    "PNJ Nu trang 14K", i['buy_nt_14k'], i['sell_nt_14k']))
            self.table.pack(pady=20)
        elif choice == "PNJ Nu trang 18K":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 18K", values=(
                    "PNJ Nu trang 18K", i['buy_nt_18k'], i['sell_nt_18k']))
            self.table.pack(pady=20)
        elif choice == "PNJ Nu trang 24K":
            self.table.delete(*self.table.get_children())
            for i in result3:
                self.table.insert(parent='', index='end', iid=None, text="PNJ Nu trang 24K", values=(
                    "PNJ Nu trang 24K", i['buy_nt_24k'], i['sell_nt_24k']))
            self.table.pack(pady=20)


# Trang đăng kí


class SigupPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="SIGUP", bg='whitesmoke', fg="red", font=(
            "times new roman", 20, "bold"))
        label_username = tk.Label(self, text="Enter your username", bg='whitesmoke', fg="green", font=("times new roman", 13, "bold"))
        label_password = tk.Label(self, text="Enter your password",bg='whitesmoke', fg="green", font=("times new roman", 13, "bold"))
        label_password_confirm = tk.Label(
            self, text="Confirm password", bg='whitesmoke', fg="green", font=("times new roman", 13, "bold"))

        self.label_notice = tk.Label(self, text="")
        self.entry_username = tk.Entry(self, width=20)
        self.entry_password = tk.Entry(self, width=20)
        self.entry_password_confirm = tk.Entry(self, width=20)

        button_Back = tk.Button(self, text="Back", bg='cornflowerblue', font=(
            "times new roman", 10, "bold"), command=lambda: appController.showPage(StartPage))
        button_Back.configure(width=10)

        self.label_notice = tk.Label(self, text="", bg="bisque2", fg='red')

        button_SignUp = tk.Button(self, text="Register", bg='cornflowerblue', font=(
            "times new roman", 13, "bold"), command=lambda: appController.signUp(self, client))
        button_SignUp.configure(width=10)

        button_Back.place(x=10, y=10)
        label_title.place(x=160, y=60)

        label_username.place(x=130, y=120)
        self.entry_username.place(x=145, y=145)

        label_password.place(x=130, y=185)
        self.entry_password.place(x=145, y=210)

        label_password_confirm.place(x=130, y=250)
        self.entry_password_confirm.place(x=145, y=275)

        self.label_notice.place(x=130, y=300)
        button_SignUp.place(x=152, y=340)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, SERVER_PORT))

app = App()
# main
app.mainloop()
