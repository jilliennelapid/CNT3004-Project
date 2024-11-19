from client import Client

class Model:
    def __init__(self):
        # Creates data fields to store commonly used data of file name and file path.
        self.filename = None
        self.filepath = None

        # Initiates an instance of the Client Class
        self.client = Client()


    def initiate_upload(self):
        # Sends file name and file path to the client side upload function
        self.client.request_upload_file(self.filename, self.filepath)
