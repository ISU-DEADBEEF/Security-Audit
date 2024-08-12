import socket

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")

        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Here, you can process the received data
                print(f"Received data: {data.decode('utf-8')}")

    server_socket.close()

if __name__ == "__main__":
    start_server()

