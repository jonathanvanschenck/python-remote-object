"""



TODO:
    - Add error logging on the server side
"""

import socketserver
import pickle

from python_remote_object.errors import TraceableError

class Server(socketserver.TCPServer):
    def __init__(self, server_address, python_object):
        socketserver.TCPServer.__init__(self, server_address, MessageHandler)
        self.pyobj = python_object
        
    def call_method(self,fname,args,kwargs):
        try:
            method = self.pyobj.__getattribute__(fname)
        except Exception as e:
            # Typically Attribute Error, but not exclusively
            return TraceableError(e)
        try:
            return_value = method(*args,**kwargs)
        except TypeError as e:
            if "not callable" in e.args[0]:
                # if method is not callable, it is an attribute
                return_value = method
            else:
                # else, some other TypeError occured which is internal to the method
                return TraceableError(e)
        except Exception as e:
            # All other internal method errors
            return TraceableError(e)
        # else, the method was successfully called
        return return_value
    
    def encode_return_value(self,return_value):
        return pickle.dumps(return_value)
    
    def parse_message(self,msg):
        fname,args,kwargs = pickle.loads(msg)
        return_value = self.call_method(fname,args,kwargs)
        return self.encode_return_value(return_value)
    
    

class MessageHandler(socketserver.StreamRequestHandler):
    
    def handle(self):
        msg = self.rfile.readline().strip()
        rmsg = self.server.parse_message(msg)
        self.wfile.write(rmsg)

