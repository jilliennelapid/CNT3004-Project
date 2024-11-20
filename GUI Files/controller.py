from client import Client

class Controller:
    def __init__(self, _view):
        self.client = Client()
        self.view = _view

    def upload(self, _filename, _filepath):
       self.client.request_upload_file(_filename, _filepath)

    def connect(self):
        if self.client:
            self.client.activate_client()

            if self.client.test_connection():
                return True
            else:
                return False

    def disconnect(self):
        if self.client:
            self.client.request_server_close()
            self.client.close_client()



