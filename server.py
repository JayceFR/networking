import socket
import threading

PORT = 5050

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) #Needs to be a tuple

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clients(conn, addr):
    print(f"{addr} connected.")
    connected = True
    while connected:
        msg = conn.recv()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print( f"Active Connections{threading.activeCount() - 1}")

print("Starting the server...")
start()
