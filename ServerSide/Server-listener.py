import socket
import os

def create_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                
                # Receive the header which contains the file path
                header_data = conn.recv(1024).decode('utf-8')
                # Splitting header_data to extract the first line as the file path
                header, _, data_start = header_data.partition('\n')
                file_path = header.strip()
                
                # Ensure the directory exists
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                print(f"Writing data to {file_path}")
                with open(file_path, "ab") as file:
                    # If there's any part of the data received along with the header, write it first
                    if data_start:
                        file.write(data_start.encode('utf-8'))
                    
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break  # Break if no more data
                        file.write(data)

                print("Data written successfully. Connection closed.")

if __name__ == "__main__":
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 83  # Arbitrary non-privileged port
    create_server(HOST, PORT)

