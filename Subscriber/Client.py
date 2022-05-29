import socket
import SubPlayer
import time
import threading

Connected=False
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.50.17.195" # Change it to the Master's ip
print(SERVER)
ADDR = (SERVER, PORT)
Player=SubPlayer.Sub()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Send():
    inp=input("Please press Any Key to quit: ")
    client.send("Disconnect!!".encode("utf-8"))



while not Connected:
    try:
        client.connect(ADDR)
        Connected=True
        thread=threading.Thread(target=Send)
        thread.start()

    except :
        print("The Server is not Connected Please wait...")
        time.sleep(1)


while Connected:
    message=client.recv(2048).decode('utf-8')
    if message=="You can leave":
        print("done")
        Connected=False
    else:
        Player.ActionToBeTaken(message)








