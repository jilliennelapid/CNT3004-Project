#tcp_server_basic.py
#!/usr/bin/env python3
import socket
import json
import os

#host binds to local server ip
host = '10.221.82.173'# some IP
port = 3300
BUFFER_SIZE = 1024  # might need to play around with buffer sizes for size of files allowed
dashes = '---->'

# Server path will be created in google cloud VM instance.
# currently a made up path !
server_path = "/path"

class Server:
    def __init__(self):
        # Creates server-side TCP socket (SOCK_STREAM) with IPv4 (AF_INET)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def activate_server(self):
        try:
            # Try to bind host to the given host address and port number.
            self.server.bind((host, port))
        except socket.error:
            return False

        # After successfully binding server, allow server to listen for messages.
        self.server.listen()

        # Will return some sort of indicator to client
        return True


    def decode_client(self, connection):
        # Receive command message on server side
        command_mess = connection.recv(BUFFER_SIZE)

        # Decode and parse JSON
        decode_mess = json.loads(command_mess.decode('utf-8'))

        command = decode_mess["command"]
        filename = decode_mess["filename"]

        if command == "UPLOAD":
            filedata = decode_mess["filedata"]

            with open(os.path.join(server_path, filename), 'w') as f:
                # Writes received data to created file
                f.write(filedata)
                # Closes created file
                f.close()

        if command == "DOWNLOAD":
            filepath = server_path + filename

            if not os.path.exists(filepath):
                return False

            # Open the file and send its content in chunks
            with open(filepath, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    self.server.send(chunk)

        if command == "DELETE":
            filepath = server_path + filename

            if os.path.exists(filepath):
                # Removes path of specified file from the directory
                os.remove(filepath)

        if command == "MKFOLDER":
            foldername = decode_mess["foldername"]

            folder_path = server_path + "/" + foldername

            os.makedirs(folder_path)

    def close_server(self):
        self.server.close()


if __name__ == "__main__":
    server_socket = Server()

    server_socket.activate_server()

    # with multithreating, call decode_client
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
    server_tcp.bind((host, port))
    #wait for client connection
    while True:
        server_tcp.listen(6)
        print('[*]Waiting for a connection')
        #establish a connection, addr = server_tcp.accept()
        with connection:
            print(f'[*] Connected from ip {addr[0]} port: {addr[1]}')
            while True:
                #data recieves bytes
                data = connection.recv(BUFFER_SIZE)
                if not data:
                    break
                else:
                    print('[*] Received data: {}' .format(data.decode('utf-8)')))
                connection.send(dashes.encode('utf-8') + data)#echo data back to origin
"""
