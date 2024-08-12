import socket
import os

def start_server(host='0.0.0.0', port=9999, log_directory='central_logs'):
    # Ensure the log directory exists
    os.makedirs(log_directory, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")

        with client_socket:
            # Receive the username and the last string
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                username, last_line = data.split(':', 1)
                log_file_path = os.path.join(log_directory, f"{username}.history")
                
                # Write the last string to the corresponding user's history file
                with open(log_file_path, 'a') as log_file:
                    log_file.write(last_line + '\n')
                print(f"Appended to {log_file_path}")

    server_socket.close()

if __name__ == "__main__":
    start_server()

