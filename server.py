import socket
import threading

class Server():
    def __init__(self) -> None:
        self.PORT = 5050
        self.HEADER = 64
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT) 
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.clients = []
    
    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER} ")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_clients, args=(conn, addr))
            thread.start()
            print( f"[Active Connections] {threading.active_count() - 1}")
    
    def handle_clients(self, conn, addr):
        self.clients.append({"whoami" : addr[1], "messages" : {}}) #messages -> {"064" : msg, "072" : msg}
        print(f"[CONNECTIONS] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                else:
                    for client in self.clients:
                        if client['whoami'] != addr[1]:
                            client['messages'][str(addr[1])] = msg
                        print(client)
                print(f"[MESSAGES] {addr} {msg}")
                conn.send("Msg received".encode(self.FORMAT))
        for pos, client in sorted(enumerate(self.clients), reverse=True):
            if client['whoami'] == addr[1]:
                self.clients.pop(pos)
        conn.close()

if __name__ == "__main__":
    server = Server()
    server.start()