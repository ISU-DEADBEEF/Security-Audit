import socket
import sys
import time

def send_file(server_host, server_port, file_path, header):
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Attempt to connect to the server
            s.connect((server_host, server_port))
            #print("Connected to server.")

            # Send the header and file path as the initial data
            initial_data = f"{header}\n{file_path}\n"
            s.sendall(initial_data.encode('utf-8'))
            
            # Open the file to read its content
            with open(file_path, 'rb') as f:
                while True:
                    # Read a chunk of the file
                    data = f.read(1024)
                    if not data:
                        break  # If no more data, stop the loop
                    # Send the chunk to the server
                    s.sendall(data)
            
            # Connection and file transfer successful
            s.close()
            #print("File sent successfully.")
            return
        except ConnectionRefusedError:
            #print("Connection refused by the server. Retrying in 3 seconds...")
            time.sleep(3)
            attempts += 1
        finally:
            # Ensure the socket is always closed
            s.close()
    
    # If unable to connect after max attempts
    #print("!!SERVER DOWN!!")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 file-sender.py <server_ip> <port> <file_path> <header>")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    header = sys.argv[4]
    
    while(True):
        send_file(server_ip, port, file_path, header)
        time.sleep(3)

