import socket
import pickle

class TaskClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def send_task(self, task_func, *args, **kwargs):
        task_data = {'func': task_func, 'args': args, 'kwargs': kwargs}
        pickled_task = pickle.dumps(task_data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.server_address, self.server_port))
                client_socket.sendall(pickled_task)

                # Receive and return result
                result = client_socket.recv(1024)
                return pickle.loads(result)
            except ConnectionRefusedError:
                print("Connection refused. Server may be down.")
            except socket.timeout:
                print("Connection timed out.")
            except pickle.PickleError as e:
                print("Error pickling/unpickling data:", e)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    client = TaskClient('192.168.19.1', 12345)
    result = client.send_task(pow, 2, 3)  # Example task: 2^3
    print("Result:", result)
