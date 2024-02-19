import socket
import threading
import pickle

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            self.send_messages()
        except Exception as e:
            print(f"Error: {e}")

    def receive_messages(self):
        while True:
            try:
                pickled_data = self.client_socket.recv(4096)
                if not pickled_data:
                    break
                message = pickle.loads(pickled_data)
                print(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        while True:
            try:
                message = input("")
                if message.lower() == 'exit':
                    break
                pickled_message = pickle.dumps(message)
                self.client_socket.sendall(pickled_message)
            except Exception as e:
                print(f"Error sending message: {e}")
                break

def main():
    host = '192.168.19.1'
    port = 12345
    client = ChatClient(host, port)
    client.start()

if __name__ == "__main__":
    main()
