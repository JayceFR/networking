import socket
import threading

PORT = 5050

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) 
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clients(conn, addr):
    print(f"[CONNECTIONS] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[MESSAGES] {addr} {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()
        
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} ")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print( f"[Active Connections] {threading.active_count() - 1}")

print("Starting the server...")
start()
