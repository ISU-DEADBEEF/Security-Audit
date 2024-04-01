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
   #             print(f"Connected by {addr}")

                # Receive the header which contains the file path
                header_data = conn.recv(1024).decode('utf-8')
                # Splitting header_data to extract the first line as the file path
                header, _, data_start = header_data.partition('\n')
                file_path = header.strip()

                # Collect all incoming data first
                all_data = data_start.encode('utf-8')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break  # Break if no more data
                    all_data += data

                # Ensure the directory exists
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Only write to the file if there's a change
                if os.path.exists(file_path):
                    with open(file_path, "rb") as existing_file:
                        existing_data = existing_file.read()
                        if existing_data != all_data:
                            with open(file_path, "wb") as file:
                                file.write(all_data)
  #                              print(f"Data written to {file_path} because of changes.")
                        else:
 #                           print("No changes detected. No write operation performed.")
                else:
                    with open(file_path, "wb") as file:
                        file.write(all_data)
#                        print(f"Data written to {file_path} as it did not exist.")

#                print("Operation complete. Connection closed.")

if __name__ == "__main__":
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 83  # Arbitrary non-privileged port
    create_server(HOST, PORT)

