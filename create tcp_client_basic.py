#TCP client basic.py
import socket
from collections.abc import Buffer
from random import seed

# client and server should match port
host = '10.221.82.173' #VM external IP
#host = '127.0.0.1'
port = 3300

BUFFER_SIZE = 1024

def setup_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_tcp:
        client_tcp.connect((host, port))
        #convert strings to bytes
        client_tcp.send(message.encode('utf-8'))#object required
        data = client_tcp.recv(BUFFER_SIZE)
        yield print(f'The message received from the server: {data.decode("utf-8")}')
        #client_tcp.close() #close not needed using 'with' context
if __name__ == '__main__':
        while True:
             message = input('Enter a message or q for quit: ')
             if message == 'q':
                quit()
             next(setup_connection())