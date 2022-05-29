import socket
import threading












def HandleClient(conn):
    msg = conn.recv(2048).decode('utf-8')
    conn.send("You can leave".encode("utf-8"))
    conn.close()
    return










def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        Clients.append(conn)
        thread = threading.Thread(target=HandleClient,args=(conn,))
        thread.start()


def Share(message):
    if(len(Clients))!=0:
        for conn in Clients:
            conn.send(message.encode("utf-8"))
            print(message)


def ShutDown():
    server.close()





Clients = []
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())# returns your local ip address
print(SERVER) # prints your local ip address
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # family= ipv4 and type is TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

thread = threading.Thread(target=start)
thread.start()







