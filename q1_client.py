import socket
import pickle

def send_file(file_path, server_host, server_port):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            filename = file_path.split('/')[-1]  # Extract filename from path
            
            # Create a dictionary to pickle
            data_to_send = {'filename': filename, 'data': file_data}
            
            # Pickle the file object
            pickled_data = pickle.dumps(data_to_send)
        
        # Create socket and connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        
        # Send pickled file object
        client_socket.sendall(pickled_data)
        
        print("File sent successfully")
    except Exception as e:
        print(f"Error: {e}")

def main():
    server_host = '192.168.19.1'
    server_port = 12345
    file_path = input("Enter the path of the file to send: ")
    
    send_file(file_path, server_host, server_port)

if __name__ == "__main__":
    main()
