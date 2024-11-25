# Client Side Code
### Requests actions for the server to do.
import socket
import json
import base64
import threading

# client and server should match port
# using localhost for testing purposes
host = "localhost"
port = 8080

BUFFER_SIZE = 1024
FORMAT = "utf-8"

class Client:
    def __init__(self):
        self.controller = None

        # Creates client-side TCP socket (SOCK_STREAM) for IPv4 (AF_INET)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_mess = ""

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
                        print(f"Server message received: {response}")

                        if mess_type == "OK":
                            print("Connection test successful: Server responded with 'OK'")
                            self.controller.statusFlag = True
                            print(f"statusFlag is now: {self.controller.statusFlag}")
                            print("updated statusflag")
                            self.controller.flag_event.set()
                        elif mess_type == "UPSTATS":
                            self.controller.send_upload_stats(payload)
                            print("Sent upload stats to controller.")
                        elif mess_type == "DOWNSTATS":
                            self.controller.send_download_stats(payload)
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

    def test_connection(self):
        test_mess = {"command": "TEST"}
        self.client.send(json.dumps(test_mess).encode(FORMAT))
        return True

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
        print("request download")

    def close_client(self):
        self.client.close()
        print("client closed")

    def request_server_close(self):
        close_mess = {"command": "END"}
        self.client.send(json.dumps(close_mess).encode(FORMAT))
        print("request to close server")