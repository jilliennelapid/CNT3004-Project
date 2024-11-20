#tcp_server_basic.py
#!/usr/bin/env python3
import socket
import json
import os

#host binds to local server ip
# using localhost for testing purposes
host = "localhost"
port = 8080
BUFFER_SIZE = 1024  # might need to play around with buffer sizes for size of files allowed
dashes = '---->'
FORMAT = 'utf-8'

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
        self.server.listen(6)

        # Server will continuously accept messages until program ends
        while True:
            conn, addr = self.server.accept()

            # with multithreating, call decode_client
            with conn:
                print("receiving message")
                self.decode_client(conn)


    def decode_client(self, connection):
        # Receive command message on server side
        command_mess = connection.recv(BUFFER_SIZE)

        # Decode and parse JSON
        decode_mess = json.loads(command_mess.decode(FORMAT))

        command = decode_mess["command"]
        try:
            filename = decode_mess["filename"]
        except KeyError:
            filename = ""

        if command == "TEST":
            connection.send("OK".encode(FORMAT))

        elif command == "END":
            # Close the connection between the client and the server
            connection.close()

        elif command == "UPLOAD":
            filedata = decode_mess["filedata"]

            with open(os.path.join(server_path, filename), 'wb') as f:
                # Writes received data to created file
                f.write(filedata)
                # Closes created file
                f.close()

        elif command == "DOWNLOAD":
            filepath = os.path.join(server_path, filename)

            if not os.path.exists(filepath):
                return False

            # Open the file and send its content in chunks
            with open(filepath, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    connection.send(chunk)

        elif command == "DELETE":
            filepath = os.path.join(server_path, filename)

            if os.path.exists(filepath):
                # Removes path of specified file from the directory
                os.remove(filepath)

        elif command == "MKFOLDER":
            foldername = decode_mess["foldername"]

            folder_path = os.path.join(server_path, foldername)

            # need to add handling overwriting files
            try:
                os.makedirs(folder_path, exist_ok=False)
            except FileExistsError as e:
                # exception for existing file
                connection.send(e)

    def close_server(self):
        self.server.close()


if __name__ == "__main__":
    server_socket = Server()

    server_socket.activate_server()

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
