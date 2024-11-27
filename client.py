# Client Side Code
### Requests actions for the server to do.
import socket
import json
import base64
import threading
import os
from pathlib import Path
# client and server should match port
# using localhost for testing purposes
host = "34.30.38.238"
port = 3389

BUFFER_SIZE = 32786
FORMAT = 'utf-8'

class Client:
    def __init__(self):
        self.controller = None

        # Creates client-side TCP socket (SOCK_STREAM) for IPv4 (AF_INET)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start_time = None

    def set_controller(self, controller):
        self.controller = controller

    def activate_client(self):
        try:
            # Try to connect to server with the given host address and port number
            self.client.connect((host, port))
        except socket.error as e:
            print(f"Error: {e}")
            # Return false for a socket connection error

        def listen_to_server():
            while True:
                try:
                    # Receive response from the server
                    response = self.client.recv(BUFFER_SIZE).decode(FORMAT)

                    if not response:
                        print("Server closed the connection.")
                        break  # Exit the loop if the server closes the connection

                    if "@" in response:
                        mess_type, payload = response.split("@")
                        print(payload)

                        if mess_type == "OK":
                            print("Connection test successful: Server responded with 'OK'")
                            self.controller.send_sys_response(payload)

                        elif mess_type == "UPSTATS":
                            self.controller.send_upload_stats(payload)

                        elif mess_type == "DOWNSTATS":
                            self.controller.send_download_stats(payload)

                        elif mess_type == "UPHIST":
                            self.controller.send_upload_hist(payload)
                            print("client received, sending to controller")

                        elif mess_type == "DOWNHIST":
                            self.controller.send_download_hist(payload)
                            print("client received, sending to controller")

                        elif mess_type == "FILERETURN":
                            self.controller.set_files(payload)

                        elif mess_type == "DOWNLOAD":
                            # Handle file download
                            self.receive_file(payload)

                        else:
                            print(f"Unknown message type: {mess_type}")
                    else:
                        print(f"Malformed message from server: {response}")
                except socket.error as e:
                    print(f"Error receiving server response: {e}")
                    break
            self.client.close()  # Ensure the client is closed when exiting the loop

        # Start the listener thread
        listener_thread = threading.Thread(target=listen_to_server, daemon=True)
        listener_thread.start()

    def receive_file(self, payload):
        # Decode and parse JSON
        decode_payload = json.loads(payload)

        filename = decode_payload["filename"]
        filedata = decode_payload["filedata"]
        decode_filedata = base64.b64decode(filedata)

        downloads_folder = os.path.join(Path.home(), "Downloads")
        filepath = os.path.join(downloads_folder, filename)

        # Ensure a unique filename if a file with the same name already exists
        if os.path.exists(filepath):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filename = f"{base}({counter}){ext}"
                filepath = os.path.join(downloads_folder, filename)
                counter += 1

        # Create directories if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write the file data
        with open(filepath, 'wb') as f:
            f.write(decode_filedata)

        print(f"File successfully saved to {filepath}")

    def test_connection(self):
        test_mess = {"command": "TEST"}
        self.client.send(json.dumps(test_mess).encode(FORMAT))
        return True

    def request_files(self):
        req_files_mess = {"command": "GETFILES"}
        self.client.send(json.dumps(req_files_mess).encode(FORMAT))

    # Sends request to create folder up to the server
    def request_create_folder(self, folderpath):
        create_fol_mess = {"command": "MKFOLDER", "folderpath": folderpath}
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
        print("Sending JSON:", json.dumps(up_file_mess))  # Verify the JSON structure being sent


    # Sends request for a file download up to the server.
    def request_download_file(self, filename):
        down_file_mess = {"command": "DOWNLOAD", "filename": filename}
        self.client.send(json.dumps(down_file_mess).encode(FORMAT))
        print("request download")

    def close_client(self):
        self.client.close()
        print("client closed")

    def request_server_close(self):
        close_mess = {"command": "END"}
        self.client.send(json.dumps(close_mess).encode(FORMAT))
        print("request to close server")