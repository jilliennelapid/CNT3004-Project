# Controller
### Facilitates communication between the GUI (view.py) and client methods (client.py)
from client import Client
import threading

class Controller:
    def __init__(self, _view):
        self.client = Client()
        self.client.set_controller(self)
        self.view = _view
        self.statusFlag = True
        self.flag_event = threading.Event()

    def upload(self, _filename, _filepath):
        self.client.request_upload_file(_filename, _filepath)

    def download(self, _filename):
        self.client.request_download_file(_filename)
        print("controller send download to client")

    def connect(self):
        if self.client:
            print("testing connection")
            self.client.activate_client()

            self.flag_event.wait(timeout=2)
            print(f"statusflag{self.statusFlag}")
            if self.client.test_connection() and self.statusFlag:
                print("connection success!!!")
                return True
            else:
                return False

    def disconnect(self):
        if self.client:
            self.client.request_server_close()
            self.client.close_client()

    def send_upload_stats(self, up_data):
        if self.client:
            self.view.display_upload_stats(up_data)
            print("sending up stats to client")

    def send_download_stats(self, down_data):
        if self.client:
            self.view.display_download_stats(down_data)