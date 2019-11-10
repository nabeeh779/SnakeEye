import socket
import sys
import threading
import DB 
import os
from shutil import copyfile

def work(msg, connection):
    db = DB.DataBase()

    code = msg[:2]
    params = getParams(msg[2:])


    if(code == "01"):# sign in 
        
        print("userName: "+params[0]+"\t password: "+params[1])

        connection.sendall(str(db.login(params[0] , params[1])).encode("utf-8"))  
		
    elif(code == '02'):# sign up

        print("userName: "+params[0]+"\t password: "+params[1])
	
        if (db.userExist(params[0]) == 0):

            db.addNewUser(params[0], params[1], params[2])
            
            id = str(db.login(params[0] , params[1]))

            copyfile(os.path.dirname(os.path.abspath(__file__)) + '\\Saves\\Copy.npy', os.path.dirname(os.path.abspath(__file__)) + '\\Saves\\' + str(id) + '.npy')

        connection.sendall(str(db.login(params[0] , params[1])).encode("utf-8"))  


    elif code == '03':# update user high score

        print("ID: "+params[0]+"\t score: "+params[1])

        db.updateUserScore(int(params[0]),int(params[1]))

    elif code == '04':# update bot high score

        print("ID: "+params[0]+"\t score: "+params[1])

        db.updateBotScore(int(params[0]),int(params[1]))

    elif code == '05':# recive bot file
        
        with open('Saves/' + params[0] + '.npy', 'wb') as f:
            while True:
                print('receiving data...')
                data = connection.recv(1024)
                print('data=%s', (data))
                if not data:
                    break
                f.write(data)

            f.close()
            connection.close()
        
        return -1

    elif code == '06':# send bot file
        
        #check in data base

        f = open('Saves/' + params[0] + '.npy','rb')
        l = f.read(1024)
        while (l):
            connection.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
        f.close()

        print('closing socket')
        connection.close()
        
        return -1
			
def getParams(msg):
	start = 0
	params = []
	
	while start < len(msg):
		currentLen = int(msg[start: start + 2])
		params.append(msg[start + 2: start + 2 + currentLen])
		start += currentLen + 2
		
	return params

def listenToClient(connection, client_address):
    try:
        print('\nconnection from', client_address)

        data = connection.recv(1024)
        print('received {!r}'.format(data))
            
        if data:
                
            print('sending data back to the client') 
            work(data.decode("utf-8"), connection)
        else:
            print('no data from', client_address)

    finally:
        # Clean up the connection
        connection.close()
        print("Client Disconnected!")
	
def main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 1000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        threading.Thread(target = listenToClient,args = (connection, client_address)).start()



main()
#print(work("0201A0312304TEST"))
#print(work("040110220"))
