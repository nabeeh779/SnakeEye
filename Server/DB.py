import sqlite3
import os

class DataBase():

    def __init__(self):
        self.conn = sqlite3.connect(os.path.dirname(__file__) + '/UserDataBase.db')#connection
        self.c = self.conn.cursor()#cursor

    def updateUserScore(self, id,newScore):
        self.c.execute('SELECT HighScore FROM T_Users WHERE ID =' + str(id))

        oldScore = int(self.c.fetchall()[0][0])

        if (newScore > oldScore):
            self.c.execute('UPDATE T_Users SET HighScore = ' + str(newScore) + ' WHERE ID = ' + str(id))
            self.conn.commit()
            return newScore
        else: 
            return oldScore

    def updateBotScore(self, id,newScore):
        self.c.execute('SELECT BotHighScore FROM T_Users WHERE ID =' + str(id))

        oldScore = int(self.c.fetchall()[0][0])

        if (newScore > oldScore):
            self.c.execute('UPDATE T_Users SET BotHighScore = ' + str(newScore) + ' WHERE ID = ' + str(id))
            self.conn.commit()
            return newScore
        else: 
            return oldScore

    def login(self, name , pas):
        self.c.execute('SELECT ID FROM T_Users WHERE UserName ="' + name +'" and Password ="' + pas +'"')
        for row in self.c.fetchall():
            return row[0]       
        return -1  

    def userExist(self, name):
        #return 1 if found and 0 if not
        self.c.execute('SELECT * FROM T_Users WHERE UserName ="' + name +'"')
        if self.c.fetchone():#tring to get the data to see if the name is found in it 
            print("User Found.")
            return 1
        else:
            print("User Doesn't exist.")
            return 0 

    def addNewUser(self, name , pas , email):
        self.c.execute('INSERT INTO T_Users (Email, UserName, Password, HighScore, BotHighScore) VALUES("' + email + '","'+ name + '","' + pas + '",0,0)')
        self.conn.commit()
        print("New User Created.")

#d = DataBase()
#addNewUser("Ohad2b","12345", "ohad041@gmail.com")
#print(d.userExist('B'))
#print(userExist("Ohad2b"))
#print(login("Ohad2b", "12345"))
#print(updateScore(1, 5))
