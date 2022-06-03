import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import *
import PIL.Image
import PIL.ImageTk

from ctypes import FormatError
from typing import Counter
import socket
import threading
import pyodbc

import json
import requests

#from ex import DISCONNECT

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
GETDOJIDATA = "getdojidata"
GETSJCDATA = "getsjcdata"
GETPNJDATA = "getpnjdata"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, SERVER_PORT))
s.listen()


def Insert_New_Account(username, password):
    cursor = ConnectToDB()
    cursor.execute(
        "insert into account(username, password) values(?,?);", username, password)
    cursor.commit()


def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while (item != "end"):
        list.append(item)
        # response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)

    return list


def check_clientSignUp(username):
    cursor = ConnectToDB()
    if username == "admin":
        return False
    cursor.execute("select username from account")
    for row in cursor:
        parse = str(row)
        parse_check = parse[2:]
        parse = parse_check.find("'")
        parse_check = parse_check[:parse]
        if parse_check == username:
            return False
    return True


Live_Account = []
ID = []
Ad = []


def Check_LiveAccount(username):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[(parse+1):]
        if parse_check == username:
            return False
    return True


def Remove_LiveAccount(conn, addr):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[:parse]
        if parse_check == str(addr):
            parse = row.find("-")
            Ad.remove(parse_check)
            username = row[(parse+1):]
            ID.remove(username)
            Live_Account.remove(row)
            conn.sendall("True".encode(FORMAT))


def check_clientLogIn(username, password):
    cursor = ConnectToDB()
    cursor.execute("select username from account")
    if Check_LiveAccount(username) == False:
        return 0
    # check if admin logged in
    if username == "admin" and password == "database":
        return 1
    cursor.execute(
        "select password from account where username=(?)", (username))
    parse = str(cursor.fetchone())
    parse_check = parse[2:]
    parse = parse_check.find("'")
    parse_check = parse_check[:parse]
    #print("1", parse_check,"1")
    if password == parse_check:
        return 2  # tk mk hop le
    return 3


def clientSignUp(sck, addr):
    username = sck.recv(1024).decode(FORMAT)
    print("Username:--" + username + "--")

    sck.sendall(username.encode(FORMAT))

    password = sck.recv(1024).decode(FORMAT)
    print("Password:--" + password + "--")

    #a = input("accepting...")
    accepted = check_clientSignUp(username)
    print("accept:", accepted)

    if accepted == True:
        Insert_New_Account(username, password)
        # add client sign up address to live account
        """ Ad.append(str(addr))
        ID.append(username)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)  """

    sck.sendall(str(accepted).encode(FORMAT))

    print("End-logIn()")
    print("")


def clientLogIn(sck):
    username = sck.recv(1024).decode(FORMAT)
    print("username:--" + username + "--")

    sck.sendall(username.encode(FORMAT))

    password = sck.recv(1024).decode(FORMAT)
    print("password:--" + password + "--")

    accepted = check_clientLogIn(username, password)
    if accepted == 2:
        ID.append(username)
        account = str(Ad[Ad.__len__()-1])+"-" + str(ID[ID.__len__()-1])
        Live_Account.append(account)

    print("Accept:", accepted)
    sck.sendall(str(accepted).encode(FORMAT))
    print("End-logIn()")
    print("")


def serverLogin(conn):
    # recv account from client
    client_account = recvList(conn)

    # query data: password
    pyodbc.cursor.execute(
        "select password from Socket_MMT where username = ?", client_account[0])
    password = pyodbc.cursor.fetchone()
    data_password = password[0]
    print(data_password)

    msg = "ok"
    if (client_account[1] == data_password):
        msg = "Login successfully"
        print(msg)

    else:
        msg = "Invalid password"
        print(msg)

    conn.sendall(msg.encode(FORMAT))


def ConnectToDB():
    server = SERVER_NAME
    database = DATABASE_NAME
    username = 'viet'
    password = '123456'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                          server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = cnxn.cursor()
    return cursor


def getAPI_DOJI():
    # Ta phải lấy API-key trước
    urlGetAPIKey = requests.get(
        'https://vapi.vnappmob.com/api/request_api_key?scope=gold')
    APIKey = urlGetAPIKey.json()['results']

    # Sau đó ta format lại chuẩn theo requirement ở trên web yêu cầu
    key = 'Bearer ' + APIKey
    # Chỉnh sửa ở header
    header = {
        'Accept': 'application/json',
        'Authorization': key
    }

    urlGetAPI = requests.get(
        "https://vapi.vnappmob.com/api/v2/gold/doji", headers=header)

    # Kết quả return là một json object, vì thế ta cần phải format nó lại về string
    return json.dumps(urlGetAPI.json())

def getAPI_SJC():
    # Ta phải lấy API-key trước
    urlGetAPIKey = requests.get(
        'https://vapi.vnappmob.com/api/request_api_key?scope=gold')
    APIKey = urlGetAPIKey.json()['results']

    # Sau đó ta format lại chuẩn theo requirement ở trên web yêu cầu
    key = 'Bearer ' + APIKey
    # Chỉnh sửa ở header
    header = {
        'Accept': 'application/json',
        'Authorization': key
    }

    urlGetAPI = requests.get(
        "https://vapi.vnappmob.com/api/v2/gold/sjc", headers=header)

    # Kết quả return là một json object, vì thế ta cần phải format nó lại về string
    return json.dumps(urlGetAPI.json())

def getAPI_PNJ():
    ## Ta phải lấy API-key trước
    urlGetAPIKey = requests.get('https://vapi.vnappmob.com/api/request_api_key?scope=gold')
    APIKey = urlGetAPIKey.json()['results']

    #Sau đó ta format lại chuẩn theo requirement ở trên web yêu cầu
    key = 'Bearer '+APIKey
    ## Chỉnh sửa ở header
    header = {
        'Accept': 'application/json',
        'Authorization': key
        }

    urlGetAPI = requests.get(
    "https://vapi.vnappmob.com/api/v2/gold/pnj",headers = header)

    ##Kết quả return là một json object, vì thế ta cần phải format nó lại về string
    return json.dumps(urlGetAPI.json())

def clientGetDOJIData(sck, addr):
    Data = getAPI_DOJI()
    sck.sendall(Data.encode(FORMAT))

def clientGetSJCData(sck, addr):
    Data = getAPI_SJC()
    sck.sendall(Data.encode(FORMAT))

def clientGetPNJData(sck, addr):
    Data = getAPI_PNJ()
    sck.sendall(Data.encode(FORMAT))


def handle_client(conn, addr):
    while True:
        option = conn.recv(1024).decode(FORMAT)
        if option == LOGIN:
            Ad.append(str(addr))
            clientLogIn(conn)
        elif option == SIGNUP:
            clientSignUp(conn, addr)
        elif option == LOGOUT:
            Remove_LiveAccount(conn, addr)
        elif option == GETDOJIDATA:
            clientGetDOJIData(conn, addr)
        elif option == GETSJCDATA:
            clientGetSJCData(conn, addr)
        elif option == GETPNJDATA:
            clientGetPNJData(conn, addr)

    Remove_LiveAccount(conn, addr)
    print("end-thread")
    conn.close()


def RunServer():
    try:
        print(HOST)
        print("Waiting for Client")

        while True:
            print("enter while loop")
            conn, addr = s.accept()

            clientThread = threading.Thread(
                target=handle_client, args=(conn, addr))
            clientThread.daemon = True
            clientThread.start()

            print("End main-loop")

    # except KeyboardInterrupt:
    #     print("Error")
    #     s.close()
    except:
        s.close()
        print("End")

# Gui-app

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Account Server")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.configure(bg="red")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage, SigupPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        self.showPage(StartPage)

    def showPage(self, container):
        frame = self.frames[container]
        if container == HomePage:
            self.geometry("600x400")
        elif container == SigupPage:
            self.geometry("600x400")
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def Login(self, curFrame, sck: socket):
        username = curFrame.entry_username.get()
        password = curFrame.entry_password.get()

        if username == "" or password == "":
            curFrame.label_notice["text"] = "Username or Password cannot be empty"
            return

        if username == "admin" and password == "server":
            self.showPage(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"



# Trang dang nhap 
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

        label_title = tk.Label(self, text="LOGIN FOR SERVER", bg='whitesmoke', fg="red", font=("times new roman", 17, "bold"))
        label_username = tk.Label(self, text="Tài khoản", bg='whitesmoke', fg="green", font=(
            "times new roman", 13, "bold"))
        label_password = tk.Label(self, text="Mật khẩu", bg='whitesmoke', fg="green", font=(
            "times new roman", 13, "bold"))

        self.label_notice = tk.Label(self, text="", bg="bisque2", fg='red')
        self.entry_username = tk.Entry(self, width=20)
        self.entry_password = tk.Entry(self, width=20)

        button_SignIn = tk.Button(self, text="Đăng nhập", bg='dodgerblue', fg="white", font=(
            "times new roman", 10, "bold"), command=lambda: Controller.Login(self, s))
        button_SignIn.configure(width=10)

        label_title.place(x=335, y=110)
        label_username.place(x=413, y=160)
        self.entry_username.place(x=390, y=185)

        label_password.place(x=413, y=215)
        self.entry_password.place(x=390, y=240)

        self.label_notice.place(x=350, y=270)

        button_SignIn.place(x=413, y=300)
        #button_SignUp.place(x=380, y=330)


# Trang hien thi thong tin
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text=" ACTIVE ACCOUNT ON SEVER ", font=(
            "times new roman", 13, "bold"), fg='red', bg="whitesmoke")
        label_title.pack()

        label_IP = tk.Label(self, text="IP: " + str(HOST),
                            font=("times new roman", 15, "bold"))
        label_IP.pack()

        self.conent = tk.Frame(self)
        self.data = tk.Listbox(self.conent, height=12, width=50, bg='floral white', activestyle='dotbox', font=("Times new Romain", 13), fg='black')

        button_log = tk.Button(self, text="REFRESH", bg="whitesmoke", command=self.Update_Client)
        button_back = tk.Button(self, text="LOG OUT", bg="whitesmoke",
                                command=lambda: controller.showPage(StartPage))
        button_back.pack(side=BOTTOM, pady=10)
        button_back.configure(width=10)
        button_log.pack(side=BOTTOM, pady=5)
        button_log.configure(width=10)

        self.conent.pack_configure()

        self.scroll = Scrollbar(self.conent)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.data.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.data.yview)

        self.data.pack(pady=10)

    def Update_Client(self):
        self.data.delete(0, len(Live_Account))
        for i in range(len(Live_Account)):
            self.data.insert(i, Live_Account[i])


# Trang đăng kí
class SigupPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="SIGUP", bg='whitesmoke', fg="red", font=(
            "times new roman", 20, "bold"))
        label_user = tk.Label(self, text="Enter your username", bg='whitesmoke',fg="green", font=("times new roman", 13, "bold"))
        label_pswd = tk.Label(self, text="Enter your password", bg='whitesmoke', fg="green", font=("times new roman", 13, "bold"))
        label_pswd_confirm = tk.Label(
            self, text="Confirm password", bg='whitesmoke', fg="green", font=("times new roman", 13, "bold"))

        self.label_notice = tk.Label(self, text="")
        self.entry_user = tk.Entry(self, width=20)
        self.entry_pswd = tk.Entry(self, width=20)
        self.entry_pswd_confirm = tk.Entry(self, width=20)

        button_Back = tk.Button(self, text="Back", bg='cornflowerblue', font=(
            "times new roman", 10, "bold"), command=lambda: appController.showPage(StartPage))
        button_Back.configure(width=10)

        button_SignUp = tk.Button(self, text="Register", bg='cornflowerblue', font=(
            "times new roman", 13, "bold"))
        button_SignUp.configure(width=10)

        button_Back.place(x=10, y=10)
        label_title.place(x=260, y=40)

        label_user.place(x=230, y=100)
        self.entry_user.place(x=245, y=125)

        label_pswd.place(x=230, y=165)
        self.entry_pswd.place(x=245, y=190)

        label_pswd_confirm.place(x=230, y=230)
        self.entry_pswd_confirm.place(x=245, y=255)

        button_SignUp.place(x=252, y=300)


sThread = threading.Thread(target=RunServer)
sThread.daemon = True
sThread.start()


app = App()
app.mainloop()
