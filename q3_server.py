import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client connected from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        with self.lock:
            self.clients.append(client_socket)
        
        while True:
            try:
                pickled_data = client_socket.recv(4096)
                if not pickled_data:
                    break
                message = pickle.loads(pickled_data)
                self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error: {e}")
                break

        with self.lock:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_socket:
                    try:
                        pickled_message = pickle.dumps(message)
                        client_socket.sendall(pickled_message)
                    except Exception as e:
                        print(f"Error broadcasting message: {e}")

def main():
    host = '192.168.19.1'
    port = 12345
    server = ChatServer(host, port)
    server.start()

if __name__ == "__main__":
    main()
