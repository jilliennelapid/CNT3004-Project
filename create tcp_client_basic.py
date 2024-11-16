#TCP client basic.py
import socket
from collections.abc import Buffer
from random import seed

# client and server should match port
host = '10.221.82.173' #VM external IP
#host = '127.0.0.1'
port = 3300

BUFFER_SIZE = 1024
FORMAT = "utf-8"

class Client:
    def __init__(self):
        # Creates a TCP socket (SOCK_STREAM) for IPv4 (AF_INET)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_connection(self):
        try:
            # Try to connect to server with the given host and port addresses
            self.client.connect((host, port))
            return True
        except socket.error:
            # Return false for a socket connection error
            return False

    # Sends request to create folder up to the server
    def request_create_folder(self):
        return

    # Sends request to delete file up to the server
    def request_delete_file(self, file):
        cmd = "DELETE"
        self.client.send(f"{cmd}@{file}".encode(FORMAT))

    # Sends request to upload file up to the server
    def request_upload_file(self, file):
        # Opens the file and reads its content in binary
        with open(f"{file}", 'rb') as f:
            # Saves the file contents to file_data
            file_data = f.read(BUFFER_SIZE)

        cmd = "UPLOAD"
        self.client.send(f"{cmd}@{file}@{file_data}".encode(FORMAT))


if __name__ == '__main__':
    """
        while True:
             message = input('Enter a message or q for quit: ')
             if message == 'q':
                quit()
             next(setup_connection())
    """


"""
#TCP client basic.py
import socket
from collections.abc import Buffer
from random import seed

# client and server should match port
host = '10.221.82.173' #VM external IP
#host = '127.0.0.1'
port = 3300

BUFFER_SIZE = 1024

def setup_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp:
        client_tcp.connect((host, port))
        #convert strings to bytes
        client_tcp.send(message.encode('utf-8'))#object required
        data = client_tcp.recv(BUFFER_SIZE)
        yield print(f'The message received from the server: {data.decode("utf-8")}')
        #client_tcp.close() #close not needed using 'with' context
if __name__ == '__main__':
        while True:
             message = input('Enter a message or q for quit: ')
             if message == 'q':
                quit()
             next(setup_connection())
"""