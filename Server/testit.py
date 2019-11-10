import sqlite3
import os

conn = sqlite3.connect('C:/Users/magshimim/SnakeDB.db')#connection
c = conn.cursor()#cursor

c.execute('SELECT id FROM info WHERE name ="' + "Man" +'" and password ="' + "123" +'"')
for row in c.fetchall():
    print row[0]        