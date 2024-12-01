# Server Side Code
### Processes Requests and performs desired actions.
### Occasionally returns data or confirmation to client-side
import socket
import json
import os
import time
import threading
import base64
import shutil
import bcrypt
from datetime import datetime

# Host and Port that Server Binds to
host = "10.128.0.3"
port = 3389

BUFFER_SIZE = 32786
dashes = '---->'
FORMAT = 'utf-8'

# Server path will be created in google cloud VM instance.
FILE_STORAGE_DIR = os.path.expanduser("~/server_files")
PASSWORD_PATH = "/home/jillienne_lapid/passwords.txt"

threads = []

# Class Server that handles server-side actions and data handling
class Server:
    def __init__(self):
        # Creates server-side TCP socket (SOCK_STREAM) with IPv4 (AF_INET)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Activates the server by binding the server to the VM instance IP address and given port
    def activate_server(self):
        try:
            # Try to bind host to the given host address and port number.
            self.server.bind((host, port))
            print("Server Bind Success!")
        except socket.error:
            return False

        # After successfully binding server, allow server to listen for messages (up to 6)
        self.server.listen(6)

        # Server will continuously accept messages until program ends
        while True:
            conn, addr = self.server.accept()

            # Threading to handle multiple client server request
            t = threading.Thread(target=self.decode_client, args=(conn,))
            t.start()
            threads.append(t)

    # Decodes the Request Messages sent from the Client
    def decode_client(self, connection):
        while True:
            try:
                # Receive command message on server side
                command_mess = connection.recv(BUFFER_SIZE)

                # Decode and parse JSON
                decode_mess = json.loads(command_mess.decode(FORMAT))

                # Get the desired command out of the JSON message
                command = decode_mess["command"]

                # If a file name is provided, save that data
                try:
                    filename = decode_mess["filename"]
                except KeyError:
                    filename = ""

                # Sends a success message to show a good connection between client and server
                if command == "TEST":
                    # Calculates the Server's Response Time
                    start_time = time.time()
                    response_time = round((time.time() - start_time), 8)

                    # Sends back an OK message to the client
                    connection.send(f"OK@{response_time}".encode(FORMAT))

                # Closes the connection and the Server
                elif command == "END":
                    # Close the connection between the client and the server
                    connection.close()
                    self.close_server()
                    break

                elif command == "VALIDATE":
                    username = decode_mess["username"]
                    password = decode_mess["password"]

                    with open(PASSWORD_PATH, "r") as file:
                        credentials_data = file.readlines()

                    for line in credentials_data:
                        stored_username, stored_hashed_password = line.strip().split(",")
                        if username == stored_username:
                            # Check if the entered password matches the stored hashed password
                            if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                                connection.send(f"VALIDATE@{True}".encode(FORMAT))
                                break

                    connection.send(f"VALIDATE@{True}".encode(FORMAT))

                elif command == "SAVE":
                    username = decode_mess["username"]
                    hashed_password = decode_mess["password"]

                    password = base64.b64decode(hashed_password)

                    credentials = f"{username},{password.decode()}\n"

                    if not os.path.exists(PASSWORD_PATH):
                        open(PASSWORD_PATH, "w").close()

                    # Save the hashed password
                    with open(PASSWORD_PATH, "a") as file:
                        file.write(credentials)

                    print("Credentials saved securely!")
                    connection.send(f"SAVE@{True}".encode(FORMAT))

                # Sends back the information of files on the server
                elif command == "GETFILES":
                    files = os.listdir(FILE_STORAGE_DIR)
                    # Send file list as JSON
                    json_files = json.dumps(files)
                    threading.Thread(target= lambda: connection.send(f"FILERETURN@{json_files}".encode('utf-8')), daemon=True).start()

                # Writes files to the file storage
                elif command == "UPLOAD":
                    start_time = time.time()  # added for upload data rate
                    filedata = decode_mess["filedata"]
                    decode_filedata = base64.b64decode(filedata)
                    filepath = os.path.join(FILE_STORAGE_DIR, filename)

                    with open(filepath, 'wb') as f:
                        # Writes received data to created file
                        f.write(decode_filedata)
                        # Closes created file
                        f.close()

                    # Get the size of the file in bytes
                    file_size = os.path.getsize(filepath)
                    end_time = time.time()

                    readable_end_time = datetime.fromtimestamp(end_time)
                    readable_start_time = datetime.fromtimestamp(end_time)

                    elapsed_time = round((end_time - start_time), 4)  # added for upload data rate
                    upload_rate = round((file_size / elapsed_time / 1_048_576), 4)  # added for upload data rate

                    stats = {"filename": filename, "uploadRate": upload_rate, "time": elapsed_time}
                    converted_stats = json.dumps(stats)
                    threading.Thread(target=lambda: connection.send(f"UPSTATS@{converted_stats}".encode(FORMAT)),
                                     daemon=True).start()

                    history_stats = {"filename": filename, "stime": readable_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                     "ctime": readable_end_time.strftime('%Y-%m-%d %H:%M:%S'), "status": "✅"}
                    converted_hist = json.dumps(history_stats)
                    threading.Thread(target=lambda: connection.send(f"UPHIST@{converted_hist}".encode(FORMAT)),
                                     daemon=True).start()

                # Gets file data and sends the data back to the client
                elif command == "DOWNLOAD":
                    start_time = time.time()
                    filepath = os.path.join(FILE_STORAGE_DIR, filename)

                    if not os.path.exists(filepath):
                        return False

                    with open(f"{filepath}", 'rb') as f:
                        # Saves the file contents to file_data
                        file_data = f.read(BUFFER_SIZE)

                    # Encode the file data to base64 for sending as JSON
                    enc_file_data = base64.b64encode(file_data).decode('utf-8')

                    # Dictionary send to server for upload file processing
                    return_mess = {"filename": filename, "filedata": enc_file_data}
                    conv_return_mess = json.dumps(return_mess)
                    # Sending the data as JSON over client socket
                    threading.Thread(target=lambda: connection.send(f"DOWNLOAD@{conv_return_mess}".encode(FORMAT)),
                                     daemon=True).start()

                    # Get the size of the file in bytes
                    file_size = os.path.getsize(filepath)
                    end_time = time.time()
                    readable_end_time = datetime.fromtimestamp(end_time)
                    readable_start_time = datetime.fromtimestamp(end_time)

                    elapsed_time = round((end_time - start_time), 4)  # added for download data rate
                    download_rate = round((file_size / elapsed_time / 1_048_576), 4) # added for download data rate

                    stats = {"filename": filename, "downloadRate": download_rate, "time": elapsed_time}
                    converted_stats = json.dumps(stats)
                    threading.Thread(target=lambda: connection.send(f"DOWNSTATS@{converted_stats}".encode(FORMAT)),
                                     daemon=True).start()

                    time.sleep(1)

                    history_stats = {"filename": filename, "stime": readable_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                     "ctime": readable_end_time.strftime('%Y-%m-%d %H:%M:%S'), "status": "✅"}
                    converted_hist = json.dumps(history_stats)
                    threading.Thread(target=lambda: connection.send(f"DOWNHIST@{converted_hist}".encode(FORMAT)),
                                     daemon=True).start()

                # Removes a file from the file storage
                elif command == "DELETE":
                    filepath = os.path.join(FILE_STORAGE_DIR, filename)

                    if os.path.exists(filepath):
                        if os.path.isfile(filepath):  # Check if it is a file
                            os.remove(filepath)  # Remove the file
                            print(f"File '{filepath}' has been deleted.")

                        elif os.path.isdir(filepath):  # Check if it is a directory
                            try:
                                shutil.rmtree(filepath)  # Remove the directory and its contents
                                print(f"Directory '{filepath}' and its contents have been deleted.")
                            except Exception as e:
                                print(f"Error deleting directory '{filepath}': {e}")
                    else:
                        print(f"Path '{filepath}' does not exist.")

                # Creates a new directory in the file storage
                elif command == "MKFOLDER":
                    folderpath = decode_mess["folderpath"]

                    try:
                        os.makedirs(folderpath, exist_ok=False)
                    except FileExistsError as e:
                        # exception for existing file
                        connection.send(f"ERROR@Another Folder already exists at the location with that name!")

            # Handles an erroneous client message
            except Exception as e:
                print(f"{dashes} Error processing client message: {e}")
                connection.send(f"ERROR: {e}".encode(FORMAT))
                break

    # Closes the Server socket
    def close_server(self):
        self.server.close()


if __name__ == "__main__":
    # Initializes the server upon running the code
    server_socket = Server()
    server_socket.activate_server()