import socket, select
from threading import Thread

HEADERLENGTH = 10
IP = '127.0.0.1'
PORT = 1234
PORT2 = 1235
DISCONNECT = '!disconnect'


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #using TCP
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((IP, PORT))

serverSocket.listen()

serverSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


serverSocket2.bind((IP, PORT2))

serverSocket2.listen()

socketList = [serverSocket]
socketList2 = [serverSocket2]

users = {}
users2 = {}

def receiveMessage(clientSocket):
    try:
        hdr = clientSocket.recv(HEADERLENGTH)

        if not len(hdr):
            return False

        msgLength = int(hdr.decode('utf-8'))
        return {'header': hdr, 'data': clientSocket.recv(msgLength)}

    except:
        return False

def room1():
    print("Starting room 1")
    while True:
        readSockets, _, exceptionSockets = select.select(socketList, [], socketList)

        
        for notifiedSocket in readSockets:
            if notifiedSocket == serverSocket:
                clientSocket, clientAddress = serverSocket.accept()

                user = receiveMessage(clientSocket)
                if user is False:
                    continue

                socketList.append(clientSocket)

                users[clientSocket] = user

                print(f"New connection: {clientAddress} user: {user['data'].decode('utf-8')} (room 1)")

            else:
                msg = receiveMessage(notifiedSocket)

                if msg is False or msg['data'].decode('utf-8') == DISCONNECT:
                    print(f"Connection closed {users[notifiedSocket]['data'].decode('utf-8')} (room 1)")
                    socketList.remove(notifiedSocket)
                    del users[notifiedSocket]
                    continue

                user = users[notifiedSocket]
                print(f"{user['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")

                for clientSocket in users:
                    if clientSocket != notifiedSocket:
                        clientSocket.send(user['header'] + user['data'] + msg['header'] + msg['data'])

        for notifiedSocket in exceptionSockets:
            socketList.remove(notifiedSocket)
            del users[notifiedSocket]

room1thread = Thread(target=room1)
room1thread.start()

def room2():
    print("Starting room 2")
    while True:
        readSockets2, _2, exceptionSockets2 = select.select(socketList2, [], socketList2)
        for notifiedSocket2 in readSockets2:
            if notifiedSocket2 == serverSocket2:
                clientSocket2, clientAddress2 = serverSocket2.accept()

                user2 = receiveMessage(clientSocket2)
                if user2 is False:
                    continue

                socketList2.append(clientSocket2)

                users2[clientSocket2] = user2

                print(f"New connection: {clientAddress2} user: {user2['data'].decode('utf-8')} (room 2)")

            else:
                msg2 = receiveMessage(notifiedSocket2)

                if msg2 is False or msg2['data'].decode('utf-8') == DISCONNECT:
                    print(f"Connection closed {users2[notifiedSocket2]['data'].decode('utf-8')} (room 2)")
                    socketList2.remove(notifiedSocket2)
                    del users2[notifiedSocket2]
                    continue

                user2 = users2[notifiedSocket2]
                print(f"{user2['data'].decode('utf-8')}: {msg2['data'].decode('utf-8')}")

                for clientSocket2 in users2:
                    if clientSocket2 != notifiedSocket2:
                        clientSocket2.send(user2['header'] + user2['data'] + msg2['header'] + msg2['data'])

        for notifiedSocket2 in exceptionSockets2:
            socketList2.remove(notifiedSocket2)
            del users2[notifiedSocket2]

room2thread = Thread(target=room2)
room2thread.start()
