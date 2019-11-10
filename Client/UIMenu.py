from tkinter import *
from tkinter import filedialog
from UIGame import *
from detailsPage import *
import UIBot
import os
import threading
import pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
window = None
tbSize = None
userId = -1
userName = ""

def singlePlayer():
    global window
    global userId
    window.withdraw()
    g = Game(0)
    points = g.RunGame()[2]
    print("Score:\t", points)
    pygame.quit()
    connection('03' + len(str(userId)) + str(userId) + len(str(points)) + str(points))
    window.deiconify()

def loadPop():
    global window
    path = filedialog.askopenfilename(initialdir = os.getcwd() + '\\Saves',title = "Select Save File",filetypes = (("Bot Saves","*.npy"),("all files","*.*")))
    
    if path.endswith(".npy"):
        window.destroy()
        UIBot.BotMenu(False, 0, path)
        main()

def newPop():
    global window
    global tbSize
    
    size = tbSize.get("1.0","end-1c")
    if size.isdigit() and int(size) > 1:
        window.destroy()
        UIBot.BotMenu(True, int(size), "")
        main()

def dsignUp():
    global window
    global userId
    global userName
    window.destroy()
    d = DetailsPage(0)
    userId, userName = d.main()
    main()

def dsignIn():
    global window
    global userId
    global userName
    window.destroy()
    d = DetailsPage(1)
    userId, userName = d.main()
    main()


def main():
    global window
    global tbSize
    global userId
    global userName

    window = Tk()
    window.title("Snake Eye Main Menu")
    window.geometry('500x500+50+50')
    lbl = Label(window, text="Snake Eye", font=("Arial Bold", 30))
    lbl.place(relx=0.5, rely=0.1, anchor=N)

    if userId == -1:
        user = Label(window, text="Guest", font=("Arial Bold", 10))
    else:
        user = Label(window, text=userName, font=("Arial Bold", 10))
    user.place(relx=0.1, rely=0.03, anchor=N)

    btn = Button(window, text="Single Player", command = singlePlayer)
    btn.place(relx=0.5, rely=0.3, anchor=N)

    btn2 = Button(window, text="Load Bot",command = loadPop)
    btn2.place(relx=0.5, rely=0.4, anchor=N)

    btn3 = Button(window, text="New Bot",command = newPop)
    btn3.place(relx=0.3, rely=0.5, anchor=N)

    btn4 = Button(window, text="Sign Up" ,command = dsignUp)
    btn4.place(relx=0.4, rely=0.6, anchor=N)

    btn5 = Button(window, text="Sign In" , command = dsignIn)
    btn5.place(relx=0.6, rely=0.6, anchor=N)

    PopSize = Label(window, text="Population Size:", font=("Arial Bold", 10))
    PopSize.place(relx=0.5, rely=0.5, anchor=N)

    tbSize=Text(window, height=1, width=5)
    tbSize.place(relx=0.7, rely=0.5, anchor=N)

    window.resizable(0, 0)

    window.mainloop()
   
if __name__ == "__main__":
    main()