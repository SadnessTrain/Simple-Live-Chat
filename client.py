import socket

HEADER=64
PORT=5050
FORMAT="UTF-8"
DISCONNECT_MESSAGE="!disconnect"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)  #need to encode message into bytes format
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)  #first message sent, representing length of actual message
    send_length+=b" "*(HEADER-len(send_length))    #b"" is byte representation of string
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


connected=True
while connected:
    user_input=input()
    send(user_input)
    if user_input==DISCONNECT_MESSAGE:
        connected=False