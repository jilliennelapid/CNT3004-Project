# Server Side Code
### Processes Requests and performs desired actions.
### Occasionally returns data or confirmation to client-side
import socket
import json
import os
import time
import threading

# host binds to local server ip
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
            print("Bind Success")
        except socket.error:
            return False

        # After successfully binding server, allow server to listen for messages.
        self.server.listen(6)

        # Server will continuously accept messages until program ends
        while True:
            conn, addr = self.server.accept()

            # with multithreating, call decode_client
            with conn:
                print("Ready to Receive Message...")
                self.decode_client(conn)

    def decode_client(self, connection):
        while True:
            try:
                # Receive command message on server side
                command_mess = connection.recv(BUFFER_SIZE)

                # Decode and parse JSON
                decode_mess = json.loads(command_mess.decode(FORMAT))

                command = decode_mess["command"]

                print(f"reached here with command: {command}.")
                try:
                    filename = decode_mess["filename"]
                except KeyError:
                    filename = ""

                if command == "TEST":
                    start_time = time.time()  # added for server response time
                    connection.send("OK@Success".encode(FORMAT))
                    response_time = time.time() - start_time  # added for server response time
                    print(f"Server response time: {response_time:.4f} seconds")  # added for server response time

                elif command == "END":
                    # Close the connection between the client and the server
                    connection.close()
                    break

                elif command == "UPLOAD":
                    print("File 'uploaded'")

                    stats = {"filename": "test.py", "uploadRate": "20", "time": "20"}
                    converted_stats = json.dumps(stats)
                    threading.Thread(target= lambda: connection.send(f"UPSTATS@{converted_stats}".encode(FORMAT)), daemon=True).start()
                    print("attempting to send back upload stats...")
                    """
                    start_time = time.time()  # added for upload data rate
                    filedata = decode_mess["filedata"]
                    filepath = os.path.join(server_path, filename)

                    with open(filepath, 'wb') as f:
                        # Writes received data to created file
                        f.write(filedata)
                        # Closes created file
                        f.close()

                    # Get the size of the file in bytes
                    file_size = os.path.getsize(filepath)

                    elapsed_time = time.time() - start_time  # added for upload data rate
                    upload_rate = file_size / elapsed_time / 1_048_576  # added for upload data rate
                    print(f"Upload data rate = {upload_rate:.2f} MB/s")  # added for upload data rate

                    stats = {"filename": filename, "uploadRate": upload_rate, "time": elapsed_time}
                    connection.send(f"UPSTATS@{stats}".encode(FORMAT))
                    """
                elif command == "DOWNLOAD":
                    print("File 'downloaded'")

                    stats = {"filename": "test.py", "uploadRate": "30", "time": "30"}
                    connection.send(f"DOWNSTATS@{stats}".encode(FORMAT))

                    """
                    start_time = time.time()  # added for download data rate
                    total_bytes_sent = 0
                    filepath = os.path.join(server_path, filename)

                    if not os.path.exists(filepath):
                        return False

                    # Open the file and send its content in chunks
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(BUFFER_SIZE):
                            connection.send(chunk)

                    # Get the size of the file in bytes
                    file_size = os.path.getsize(filepath)

                    elapsed_time = time.time() - start_time  # added for download data rate
                    download_rate = file_size / elapsed_time / 1_048_576  # added for download data rate
                    stats = {"filename": filename, "uploadRate": download_rate, "time": elapsed_time}
                    connection.send(f"DOWNSTATS@{stats}".encode(FORMAT))
                    """
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
            except Exception as e:
                print(f"{dashes} Error processing client message: {e}")
                connection.send(f"ERROR: {e}".encode(FORMAT))
                break

    def close_server(self):
        self.server.close()


if __name__ == "__main__":
    server_socket = Server()

    server_socket.activate_server()