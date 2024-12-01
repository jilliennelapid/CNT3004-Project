# Controller
### Facilitates communication between the GUI (view.py) and client methods (client.py)
from client import Client
import time

# Class Controller that assists communication between the GUI and the client
class Controller:
    def __init__(self, _view):
        # Instantiates a client instance for access to client functions
        self.client = Client()
        self.client.set_controller(self)
        self.view = _view

        self.statusFlag = None      # Flag for checking server connection
        self.sys_res_time = None    # Flag for setting system response time


    """ Main Functionality Methods """
    # Helps make a client request to Connect to the Server
    def connect(self):
        if self.client:
            print("Testing Connection...")
            self.client.activate_client()               # Attempts to connect client and server

            if self.client.test_connection():           # If connection successful, set flag
                time.sleep(2)
                if self.statusFlag:
                    return True
            else:
                return False

    # Helps make a client request to Disconnect from the Server
    def disconnect(self):
        if self.client:
            self.client.request_server_close()
            self.client.close_client()

    # Helps make a client request for Uploading a File
    def upload(self, _filename, _filepath):
        self.client.request_upload_file(_filename, _filepath)

    # Helps make a client request for Downloading a File
    def download(self, _filename):
        self.client.request_download_file(_filename)

    # Helps make a client request for Deleting a File/Folder
    def delete(self, _filename):
        self.client.request_delete_file(_filename)

    # Helps make a client request for Creating a Folder on the server
    def makedir(self, _filepath):
        self.client.request_create_folder(_filepath)


    """ Methods for Sending Data back to the GUI """
    # Sends back the system response time to the GUI
    def send_sys_response(self, payload):
        self.statusFlag = 1
        self.sys_res_time = payload
        print(f"{self.statusFlag} and {self.sys_res_time}")

    # Sends back the Upload Statistics to the GUI
    def send_upload_stats(self, up_data):
        if self.client:
            self.view.display_upload_stats(up_data)

    # Sends back the Download Statistics to the GUI
    def send_download_stats(self, down_data):
        if self.client:
            self.view.display_download_stats(down_data)

    # Sends back the Upload History to the GUI
    def send_upload_hist(self, data):
        if self.client:
            self.view.update_upload_history(data)

    # Sends back the Download History to the GUI
    def send_download_hist(self, data):
        if self.client:
            self.view.update_download_history(data)

    # Gets the Files on the Server for the GUI
    def get_files(self):
        if self.client:
            self.client.request_files()

    # Sends back the Files on the Server to the GUI
    def set_files(self, files):
        if self.client:
            self.view.return_files(files)