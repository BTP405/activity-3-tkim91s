import socket
import pickle
import threading

class WorkerNode:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.server_address, self.server_port))
            server_socket.listen(5)

            print("Worker node waiting for tasks...")

            while True:
                conn, addr = server_socket.accept()
                print("Connected by", addr)

                threading.Thread(target=self.handle_task, args=(conn,)).start()

    def handle_task(self, conn):
        with conn:
            try:
                task_data = conn.recv(1024)
                task = pickle.loads(task_data)
                result = self.execute_task(task)
                conn.sendall(pickle.dumps(result))
            except pickle.UnpicklingError as e:
                print("Error unpickling data:", e)
            except Exception as e:
                print("Error:", e)

    def execute_task(self, task):
        func = task['func']
        args = task['args']
        kwargs = task['kwargs']
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print("Error executing task:", e)

if __name__ == "__main__":
    worker = WorkerNode('192.168.19.1', 12345)
    worker.start()
