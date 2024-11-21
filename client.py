#TCP client basic.py
import socket
import json
import base64
from collections.abc import Buffer
from random import seed
import time
# client and server should match port
# using localhost for testing purposes
host = "localhost"
port = 8080

BUFFER_SIZE = 1024
FORMAT = "utf-8"

class Client:
    def __init__(self):
        # Creates client-side TCP socket (SOCK_STREAM) for IPv4 (AF_INET)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_mess = ""
    def activate_client(self):
        try:
            # Try to connect to server with the given host address and port number
            self.client.connect((host, port))
        except socket.error as e:
            print(f"Error: {e}")
            # Return false for a socket connection error

    def test_connection(self):
        test_mess = {"command": "TEST"}
        self.client.send(json.dumps(test_mess).encode(FORMAT))

        # Receive response from the server
        try:
            # Look for response from the server
            response = self.client.recv(BUFFER_SIZE).decode(FORMAT)

            # If "OK" response, then connection is good
            if response == "OK":
                print("Connection test successful: Server responded with 'OK'")
                return True
            else:
                print(f"Connection test failed: Unexpected response '{response}'")
                return False
        except socket.error as e:
            print(f"Error receiving server response: {e}")
            return False


    # Sends request to create folder up to the server
    def request_create_folder(self, folderName):
        create_fol_mess = {"command": "MKFOLDER", "filename": folderName}
        self.client.send(json.dumps(create_fol_mess).encode(FORMAT))

    # Sends request to delete file up to the server.
    def request_delete_file(self, filename):
        del_file_mess = {"command": "DELETE", "filename": filename}
        self.client.send(json.dumps(del_file_mess).encode(FORMAT))

    # Sends request to upload file up to the server.
    def request_upload_file(self, filename, filepath):
        # Opens the file and reads its content in binary
        with open(f"{filepath}", 'rb') as f:
            # Saves the file contents to file_data
            file_data = f.read(BUFFER_SIZE)

        # Encode the file data to base64 for sending as JSON
        enc_file_data = base64.b64encode(file_data).decode('utf-8')

        # Dictionary send to server for upload file processing
        up_file_mess = {"command": "UPLOAD", "filename": filename, "filedata": enc_file_data}

        # Sending the data as JSON over client socket
        print(f"Sending file {filename}")
        self.client.send(json.dumps(up_file_mess).encode(FORMAT))

    # Sends request for a file download up to the server.
    def request_download_file(self, filename):
        down_file_mess = {"command": "DOWNLOAD", "filename": filename}
        self.client.send(json.dumps(down_file_mess).encode(FORMAT))

    def close_client(self):
        self.client.close()
        print("client closed")

    def request_server_close(self):
        close_mess = {"command": "END"}
        self.client.send(json.dumps(close_mess).encode(FORMAT))
        print("request to close server")

"""
if __name__ == '__main__':
    client_socket = Client()

    client_socket.activate_client()

    
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
