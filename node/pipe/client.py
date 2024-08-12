import os
import socket

def send_history_files(server_host='localhost', server_port=9999):
    # Define the directory path
    directory_path = "/var/log/Logger"

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        # Iterate over all files in the directory
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)

            # Check if it is a file and ends with .history
            if os.path.isfile(file_path) and file_name.endswith('.history'):
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    client_socket.sendall(file_content.encode('utf-8'))
                    print(f"Sent file: {file_name}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    send_history_files()

