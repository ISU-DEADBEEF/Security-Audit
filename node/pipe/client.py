import os
import socket

def send_last_line_from_files(server_host='localhost', server_port=9999):
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
                username = file_name.split('.')[0]
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        # Send the username and the last line
                        message = f"{username}:{last_line}"
                        client_socket.sendall(message.encode('utf-8'))
                        print(f"Sent last line from {file_name}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    send_last_line_from_files()

