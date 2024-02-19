import socket
import pickle
import os

def receive_file(server_socket, save_directory):
    try:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        
        # Receive pickled file object
        pickled_data = client_socket.recv(4096)
        file_data = pickle.loads(pickled_data)
        
        # Extract filename from file object
        filename = os.path.basename(file_data['filename'])
        
        # Save the file to specified directory
        save_path = os.path.join(save_directory, filename)
        with open(save_path, 'wb') as f:
            f.write(file_data['data'])
        
        print(f"File received and saved to {save_path}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    host = '192.168.19.1'
    port = 12345
    save_directory = './received_files'
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Server listening on {host}:{port}")
    
    while True:
        receive_file(server_socket, save_directory)

if __name__ == "__main__":
    main()
