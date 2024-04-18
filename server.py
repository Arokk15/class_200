# import 
import socket
from threading import Thread

# create a socket for server
# 1. IPV4
# 2. TCP
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind( (ip_address,port) )
server.listen()

list_of_clients = []
nicknames=[]
print("Server has started....")

def clientThread(conn,nickname):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                print(message)
                broadcast(message , conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def broadcast(message,connection):
    for i in list_of_clients:
        if i!=connection:
            try:
                i.send(message.encode("utf-8"))
            except:
                remove(i)

def remove(connection):
    for i in list_of_clients:
        list_of_clients.remove(i)


def remove_nickname(nickname):
    for i in nicknames:
        nicknames.remove(i)

while True:
    conn , addr =server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    #print(conn , addr)
    list_of_clients.append(conn)
    #print(addr[0]+" connected to the server....")
    
    message="{} joined".format(nickname)
    print(message)
    broadcast(message,conn)

    newThread = Thread(target=clientThread , args=(conn , nickname))
    newThread.start()