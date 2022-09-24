import socket
import threading

#you can import an use pickle to send whole python objects

HEADER=64   #first message from client is always header, and says how many bytes next one will be
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())   #gets your ip
ADDR=(SERVER,PORT)  #tuple for binding socket to adress
FORMAT="UTF-8"
DISCONNECT_MESSAGE="!disconnect"
NICKNAME_MESSAGE="!nickname"
NICKNAME=""

PING_MESSAGE="!ping"
client_LAST_MESSAGE=""

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #(family,type)
server.bind(ADDR)

#make thread/protocol that stores all messages sent to server in a list, and sent them to all connected clients
#alternative: have cliends send a ping command that constantly asks if a new message has been sent, if yes it send that back. think this still uses the list

all_connections=[]
all_messages=[]

def update_chat():
    global client_LAST_MESSAGE

    print("test update chat")
    if len(all_messages)>0:
        if all_messages[-1] != client_LAST_MESSAGE:
            for user in all_connections:
                user.send(all_messages[-1].encode(FORMAT))
                client_LAST_MESSAGE = all_messages[-1]
    else:
        for user in all_connections:
            user.send("".encode(FORMAT))

def handle_client(conn, addr):  #handle individual connections between client and server
    print(f"[NEW CONNECTION] {addr} connected.")
    all_connections.append(conn)
    global NICKNAME
    NICKNAME=addr

    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)     #this line of code will NOT be passsed until it recieves a message. this is called a blocking line
        #need to know how many bytes of message you recieve, so you make a protocol to find out
        if msg_length:  #if message not empty(some empty message is sent on connect)
            msg_length=int(msg_length)  #header is in bytes so convert to int
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg!=PING_MESSAGE:
                if msg[0]=="!":
                    if msg.split()[0]==NICKNAME_MESSAGE:
                        NICKNAME=msg.split()[1]
                    elif msg==DISCONNECT_MESSAGE:
                        connected=False
                        all_connections.remove(conn)
                else:
                    all_messages.append(f"[{NICKNAME}]: {msg}")
                    print(f"[{NICKNAME}]: {msg}")
            if msg==PING_MESSAGE:
                update_chat()

    conn.close()

def start():    #start listening to connections and pass them to handle_client
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()    #wait for new connection, when happens, store where it came from
        thread = threading.Thread(target=handle_client, args=(conn,addr))    #start new copy of function
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")    #start thread is always running so -1

print("[STARTING] Server is starting...")
start()