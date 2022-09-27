import socket
import threading
import time

import select

NICKNAME=input("Input nickname to use during chatting (no spaces!):\n")

HEADER=64
PORT=5050
FORMAT="UTF-8"
DISCONNECT_MESSAGE="!disconnect"
PING_MESSAGE="!ping"
SERVER=input("Input IP of user you want to connect to:\n")
ADDR=(SERVER,PORT)
connected=False

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def ping():
    send(PING_MESSAGE)
    ready = select.select([client], [], [], 0.5)
    if ready[0]:
        print(client.recv(2048).decode(FORMAT))


def send(msg):
    message=msg.encode(FORMAT)  #need to encode message into bytes format
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)  #first message sent, representing length of actual message
    send_length+=b" "*(HEADER-len(send_length))    #b"" is byte representation of string
    client.send(send_length)
    client.send(message)

send("!nickname "+NICKNAME)

def connect():
    global connected
    connected = True

    while connected:
        user_input=input()
        send(user_input)
        if user_input==DISCONNECT_MESSAGE:
            connected=False

threading.Thread(target=connect).start()
while connected:
    ping()