from GeneticAlgorithm import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import threading
import os

gn = None
tbLoops = None
root = None
tbGen = {}

def BotMenu(newPop = True, popSize = 0, path = ""):
    global tbLoops
    global root
    global tbGen

    tbGen = {}

    root = Tk()
    root.title("Snake Eye Main Menu")
    root.geometry('500x500+50+50')

    #headline label

    lbl = Label(root, text="Snake Eye", font=("Arial Bold", 30))
    lbl.place(relx=0.5, rely=0.1, anchor=N)

    #run game interface

    btn3 = Button(root, text="Play",command = runGame)
    btn3.place(relx=0.3, rely=0.3, anchor=N)
    
    Loops = Label(root, text="Game Runs:", font=("Arial Bold", 7))
    Loops.place(relx=0.5, rely=0.3, anchor=N)

    tbLoops=Text(root, height=1, width=5)
    tbLoops.delete(1.0, END)
    tbLoops.insert(END, 3)
    tbLoops.place(relx=0.7, rely=0.3, anchor=N)

    #genetic algorithm interface

    btn2 = Button(root, text="Evolve",command = runEvolve)
    btn2.place(relx=0.3, rely=0.4, anchor=N)
    
    Loops2 = Label(root, text="Generations:", font=("Arial Bold", 7))
    Loops2.place(relx=0.5, rely=0.4, anchor=N)

    tbTemp=Text(root, height=1, width=5)
    tbTemp.delete(1.0, END)
    tbTemp.insert(END, 50)
    tbTemp.place(relx=0.7, rely=0.4, anchor=N)
    tbGen['loops'] = tbTemp
   
    temp = Label(root, text="Score per point:", font=("Arial Bold", 7))
    temp.place(relx=0.4, rely=0.5, anchor=N)

    tbTemp=Text(root, height=1, width=5)
    tbTemp.delete(1.0, END)
    tbTemp.insert(END, 50)
    tbTemp.place(relx=0.6, rely=0.5, anchor=N)
    tbGen['eat'] = tbTemp

    temp = Label(root, text="Score per death:", font=("Arial Bold", 7))
    temp.place(relx=0.4, rely=0.6, anchor=N)

    tbTemp=Text(root, height=1, width=5)
    tbTemp.delete(1.0, END)
    tbTemp.insert(END, -10)
    tbTemp.place(relx=0.6, rely=0.6, anchor=N)
    tbGen['death'] = tbTemp

    temp = Label(root, text="Score per good move:", font=("Arial Bold", 7))
    temp.place(relx=0.4, rely=0.7, anchor=N)

    tbTemp=Text(root, height=1, width=5)
    tbTemp.delete(1.0, END)
    tbTemp.insert(END, 1)
    tbTemp.place(relx=0.6, rely=0.7, anchor=N)
    tbGen['goodMove'] = tbTemp

    temp = Label(root, text="Score per bad move:", font=("Arial Bold", 7))
    temp.place(relx=0.4, rely=0.8, anchor=N)

    tbTemp=Text(root, height=1, width=5)
    tbTemp.delete(1.0, END)
    tbTemp.insert(END, -2)
    tbTemp.place(relx=0.6, rely=0.8, anchor=N)
    tbGen['badMove'] = tbTemp

    #save bot button

    btn = Button(root, text="Save Bot",command = saveBot)
    btn.place(relx=0.5, rely=0.9, anchor=N)

    #loading label

    lbl2 = Label(root, text="Loading", font=("Arial Bold", 7))
    lbl2.grid(column=0, row=0)

    root.resizable(0, 0)

    ThreadLoad = threading.Thread(target=loadGn, args=(newPop, popSize, path, lbl2))
    ThreadLoad.start()

    root.protocol("WM_DELETE_WINDOW", ask_quit)
    root.mainloop()


def ask_quit():
    global root
    if messagebox.askokcancel("Quit", "Are You Sure You Want To Quit Now?\nAll unsaved changes will be lost."):
        root.destroy()

def runEvolve():
    global tbGen
    global gn

    epoch = tbGen['loops'].get("1.0","end-1c")
    gn.scoring = getScoring()

    if epoch.isdigit() and int(epoch) > 0:

        gn.evolving = True    
        ThreadEvolve = threading.Thread(target=EvolveDisply)
        ThreadEvolve.start()

        for i in range(int(epoch)):
            print("Generation", i + 1, "Run!\n")
            gn.evolve()
            if not gn.evolving:
                break

        gn.pop = gn.grade()

        gn.evolving = False

def EvolveDisply():
    global gn

    while gn.evolving:
        g = Game(gn.pop[0], True, gn.params, 100)
        _ , UserExit, _ = g.RunGame()
        if UserExit:
            gn.evolving = False
    
    pygame.quit()
    return

def getScoring():
    global tbGen
    scoring = {}

    scoring['eat'] = int(tbGen['eat'].get("1.0","end-1c"))
    scoring['death'] = int(tbGen['death'].get("1.0","end-1c"))
    scoring['goodMove'] = int(tbGen['goodMove'].get("1.0","end-1c"))
    scoring['badMove'] = int(tbGen['badMove'].get("1.0","end-1c"))

    return scoring

def runGame():
    global tbLoops
    games = tbLoops.get("1.0","end-1c")

    if games.isdigit() and int(games) > 0:
        for i in range(int(games)):
            g = Game(gn.pop[0], True, gn.params)
            _ , UserExit, points = g.RunGame()
            if UserExit:
                break

    pygame.quit()
    
def loadGn(newPop, popSize, path, lbl2):
    global gn
    gn = GeneticAlgorithm()

    if newPop:
        gn.create_population(popSize)
    else:
        gn.load_network(path)

    lbl2.destroy()

    return 


def saveBot():
    global gn
    gn.save_network(filedialog.asksaveasfilename(initialdir = os.getcwd() + '\\Saves',title = "Save Bot",filetypes = (("Bot Saves","*.npy"),("all files","*.*"))))