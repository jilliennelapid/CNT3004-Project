# Controller
### Facilitates communication between the GUI (view.py) and client methods (client.py)
from client import Client
import time

class Controller:
    def __init__(self, _view):
        self.client = Client()
        self.client.set_controller(self)
        self.view = _view

        self.statusFlag = None
        self.sys_res_time = None

    def upload(self, _filename, _filepath):
        self.client.request_upload_file(_filename, _filepath)

    def download(self, _filename):
        self.client.request_download_file(_filename)

    def delete(self, _filename):
        self.client.request_delete_file(_filename)

    def makedir(self, _filepath):
        self.client.request_create_folder(_filepath)

    def send_sys_response(self, payload):
        self.statusFlag = 1
        self.sys_res_time = payload
        print(f"{self.statusFlag} and {self.sys_res_time}")

    def connect(self):
        if self.client:
            print("testing connection")
            self.client.activate_client()

            if self.client.test_connection():
                print(f"statusFlag: {self.statusFlag}")
                time.sleep(2)
                if self.statusFlag:
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

    def send_download_stats(self, down_data):
        if self.client:
            self.view.display_download_stats(down_data)

    def send_upload_hist(self, data):
        if self.client:
            self.view.update_upload_history(data)

    def send_download_hist(self, data):
        if self.client:
            self.view.update_download_history(data)
            print("controller received, sending to view")

    def get_files(self):
        if self.client:
            self.client.request_files()

    def set_files(self, files):
        if self.client:
            self.view.return_files(files)