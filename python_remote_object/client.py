"""

TODO:
    - Modify timeout functionality to allow longer timescale method calls
    - Add secondary client method which allows method calls on the server 
        (not just the pyobj wrapped by the server)
"""

import socket
import pickle

from python_remote_object.errors import CallMethodError

BUFFER_SIZE = 1024
TIMEOUT = 3

class Client:
    def __init__(self,ip,port):
        self.__ip,self.__port = ip,port
    
    def __repr__(self):
        try:
            _repr = self.__call_method("__repr__")
        except:
            _repr = "pointed at {0}:{1}".format(self.__ip,self.__port)
        return "<Remote Wrapper {}>".format(_repr)
    
    def __call_method(self,fname,*args,**kwargs):
        socket = MessageSocket(self.__ip,self.__port)
        rmsg = socket.send_message(pickle.dumps((fname,args,kwargs)))
        socket.close()
        return_value = pickle.loads(rmsg)
        if isinstance(return_value, Exception):
            raise CallMethodError("Remote Method Call Failed") from return_value()
        return return_value
    
    def __getattr__(self,key):
        def f(*args,**kwargs):
            return self.__call_method(key,*args,**kwargs)
        return f

class MessageSocket(socket.socket):
    def __init__(self,ip,port):
        socket.socket.__init__(self,socket.AF_INET,
                               socket.SOCK_STREAM)
        self.settimeout(TIMEOUT)
        self.connect((ip,port))
        
    def send_message(self,msg):
        self.sendall(msg + b'\n')
        self.buffer = b''
        while True:
            rmsg = self.recv(BUFFER_SIZE)
            if rmsg == b'':
                break
            self.buffer = self.buffer + rmsg
        return self.buffer.strip()
