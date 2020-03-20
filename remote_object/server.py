# TODO:
#     - Add error logging on the server side

import socketserver
import pickle

from .errors import TraceableError

class Server(socketserver.TCPServer):
    """A remote_object server.Server object
    
    This class is intended to host a python object so that 
    method calls made on a client.Client instance pointed at
    this server can be forwaded here and applied to .pyobj,
    any return values/errors resulting from that call are
    passed back to the client and are returned/raised there.
    
    This class inherits from a socketserver.TCPserver object.
    The main extensions of the class is to hold a reference to
    some generic python object, and add the .call_method method,
    which handles calls, errors and returns.
    
    :param server_address: a tuple containing the address and port
                            on which to host the server: (IP, PORT)
    
    :param pyobj: a reference to python object which will be hosted 
                    by the server. Any method calls made by a client
                    will be applied to this object, and all values/errors
                    it produces will be returned/raised.
    
    Example Usage::
        
        import time
        
        sever.Server(('some ip',9999),time) as server:
            # Set server up to accept connections forever,
            #  clients may now check the server's processor
            #  time, locally callable as time.time(), by
            #  calling: client.Client('some ip', 9999).time()
            server.serve_forever()
    """
    def __init__(self, server_address, python_object):
        socketserver.TCPServer.__init__(self, server_address, MessageHandler)
        self.pyobj = python_object
        
    def call_method(self,fname,args,kwargs):
        """Handler for method calls on .pyobj
        
        This method handles all attempted method calls on the .pyobj.
        There are three main cases:
            1) the requested method does not exist, causes an error
                or is called with an incorrect signiture
                => Catch the error and return it with its traceback
            2) the requested 'method' is actually and attribute
                => ignore the call signiture and return the attribute
            3) the requested method is successfully called
                => return any resulting values 
        """
        try:
            method = self.pyobj.__getattribute__(fname)
        except Exception as e:
            # Typically AttributeError, if .pyobj does not have
            #  the requested method
            return TraceableError(e)
        
        try:
            return_value = method(*args,**kwargs)
        except TypeError as e:
            if "not callable" in e.args[0]:
                # If 'method' is not callable, it is an attribute.
                #  assuming the .pyobj doesn't itself mistakenly
                #  call an uncallable object in the method.
                return_value = method
            else:
                # Else, some other TypeError occured which is internal
                #  to the .pyobj method which was called
                return TraceableError(e)
        except Exception as e:
            # All other internal .pyobj method errors
            return TraceableError(e)
        
        # Else, the method was successfully called
        return return_value
    
    #def encode_return_value(self,return_value):
    #    return pickle.dumps(return_value)
    #def decode_message(self,msg):
    #    return pickle.loads(msg)
    
    def parse_message(self,msg):
        """Parses incoming messages and encodes return values
        """
        fname,args,kwargs = pickle.loads(msg)#self.decode_message(self,msg)
        return_value = self.call_method(fname,args,kwargs)
        return pickle.dumps(return_value)#self.encode_return_value(return_value)
    
    

class MessageHandler(socketserver.StreamRequestHandler):
    """MessageHandler class for server.Server instance.
    
    This class inherts from the socket.server.StreamRequestHandler,
    see the socketserver documentation for details about its
    use in a socketserver.TCPServer object (from which the server.Server
    inherits).
    
    The main overriden method from the base class is .handle(), which
    gets the message send by a client TCP socket connection and passes
    it to the server.Server instance for parsing. The server returns
    a pre-encoded return message, which the handler then passes back
    to the client over the same TCP socket.
    """
    def handle(self):
        msg = self.rfile.readline().strip()
        rmsg = self.server.parse_message(msg)
        self.wfile.write(rmsg)

