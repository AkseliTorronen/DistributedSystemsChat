import socket, select, errno, sys

HEADERLENGTH = 10
IP = '127.0.0.1'
PORT = 1234
PORT2 = 1235
DISCONNECT = '!disconnect'

username = input("Enter username: ")
room = int(input("Which chat room 1 or 2: "))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if room==1:
    clientSocket.connect((IP, PORT)) #connect to room 1
else:
    clientSocket.connect((IP, PORT2)) #connect to room 2
clientSocket.setblocking(False)

currentUser = username.encode('utf-8')
usernameHeader = f"{len(currentUser):<{HEADERLENGTH}}".encode('utf-8')
clientSocket.send(usernameHeader + currentUser)


while True:
    msg = input(f"{username}: ")
    

    if msg:
        msge = msg
        msg = msg.encode('utf-8')
        msgHeader = f"{len(msg):<{HEADERLENGTH}}".encode('utf-8')
        clientSocket.send(msgHeader + msg)
        if msge == '!disconnect':
            sys.exit()
    
    try:
        while True:
            usernameHeader = clientSocket.recv(HEADERLENGTH)
            if not len(usernameHeader):
                print("Connection closed by the server")
                sys.exit()
            usernameLength = int(usernameHeader.decode('utf-8').strip())
            currentUser = clientSocket.recv(usernameLength).decode('utf-8')

            msgHeader = clientSocket.recv(HEADERLENGTH)
            msgLength = int(msgHeader.decode('utf-8').strip())
            msg = clientSocket.recv(msgLength).decode('utf-8')

            print(f"{currentUser}: {msg}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error: ",str(e))
            sys.exit()
        continue

    except Exception as e:
        print("Ran into an error: ",str(e))
        sys.exit()

