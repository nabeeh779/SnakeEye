from tkinter import *
from tkinter import messagebox
import UIMenu 
import socket
import sys

tbSize = None

class DetailsPage():

    def __init__(self, windowType):
        self.type = windowType
        self.window = None
        self.name = ""
        self.id = -1

    def main(self):
        
        #installing the gui using tkinter
        self.window  = Tk()
        self.window.title("Snake Eye Main Menu")
        self.window.geometry('500x500+50+50')

        lbl = Label(self.window, text="Snake Eye ", font=("Arial Bold", 30))
        lbl.place(relx=0.5, rely=0.1, anchor=N)

        self.passwordInput = Text(self.window, height=1, width=15)
        self.nameInput = Text(self.window, height=1, width=15)

        UserName = Label(self.window, text="UserName:", font=("Arial Bold", 10))
        UserName.place(relx=0.4, rely=0.3, anchor=N)
        self.nameInput.place(relx=0.65, rely=0.3, anchor=N)

        password = Label(self.window, text="Password:", font=("Arial Bold", 10))
        password.place(relx=0.4, rely=0.4, anchor=N)
        self.passwordInput.place(relx=0.65, rely=0.4, anchor=N)

        if self.type == 1:
            subBtn = Button(self.window, text="submit" , command = self.subSignIn)
            subBtn.place(relx=0.5, rely=0.5, anchor=N)

        else:   
            Email = Label(self.window, text="Email:", font=("Arial Bold", 10))
            Email.place(relx=0.4, rely=0.5, anchor=N)

            self.EmailInput = Text(self.window, height=1, width=15)
            self.EmailInput.place(relx=0.65, rely=0.5, anchor=N)

            subBtn = Button(self.window, text="submit" ,command = self.subSignUp)
            subBtn.place(relx=0.5, rely=0.6, anchor=N)

        self.window.mainloop()

        return self.id, self.name
   
    def subSignIn(self):
        global detailsPage
        name = self.nameInput.get("1.0","end-1c")
        pas = self.passwordInput.get("1.0","end-1c")

        res = connection('01' + str(len(name)).zfill(2) + name + str(len(pas)).zfill(2) + pas)
        if (res != -1):
            print("sign in done")
            self.id = res
            self.name = name
            self.window.destroy()

        else:
            print("wrong details")
            messagebox.showerror("Error", "userName or password is incorrect ")
        
    def subSignUp(self):
    # global nameInput
        name = self.nameInput.get("1.0","end-1c")
        pas = self.passwordInput.get("1.0","end-1c")
        em = self.EmailInput.get("1.0","end-1c")

        res = connection('02' + str(len(name)).zfill(2) + name + str(len(pas)).zfill(2) + pas + str(len(em)).zfill(2) + em)
        if (res != -1):
            print("new user")
            self.id = res
            self.name = name
            self.window.destroy()

        else:
            print("user exist / wrong details")
            messagebox.showerror("Error", "User already existed ")

def connection(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    amount_received = 0
    server_address = ('localhost', 1000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    data = -1

    try:
        print('sending', message)
        sock.sendall(message.encode('utf-8'))

        data = sock.recv(4).decode('utf-8')
        amount_received += len(data)
        print('received', data)

    finally:
        print('closing socket')
        sock.close()
        return data