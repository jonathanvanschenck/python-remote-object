'''
Run this script in two different terminals:
    1) python simple_class.py server
    2) python simple_class.py client
'''

from sys import argv
from remote_object.server import Server
from remote_object.client import Client

HOST, PORT = 'localhost', 9999

class PythonObject:
    def __init__(self):
        self.a = "ra"
        
    def b(self):
        return "rb"
    
    def __repr__(self):
        return "<Generic Python Object>"



if __name__ == "__main__" and argv[1] == "server":
    with Server((HOST, PORT), PythonObject()) as server:
        print("Hosting at: {0}|{1}".format(HOST,PORT))
        server.serve_forever()
      
elif __name__ == "__main__" and argv[1] == "client":
    client = Client(HOST, PORT)
    print(client) # prints: <Remote Wrapper <Generic Python Object>>    
    print(client.a()) # prints ra
    print(client.b()) # prints rb
    print(client.c()) # raises CallMethodError
