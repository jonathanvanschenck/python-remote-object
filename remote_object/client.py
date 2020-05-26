# TODO:
#     - Modify timeout functionality to allow longer timescale method calls
#     - Add secondary client method which allows method calls on the server
#         (not just the pyobj wrapped by the server)

import socket
import pickle

from .errors import CallMethodError as _CallMethodError

def mixin_error(error,msg=""):
    # Create new error which inherits from both the base
    #  class and _CallMethodError, so the new error can
    #  be caught by both execpt types
    class CallMethodError(error__class__,_CallMethodError):
        pass
    return CallMethodError(msg)

# The choice of BUFFER_SIZE and TIMEOUT are somewhat arbitrary,
#  it would be good in the future to test some ideal values,
#  or at least let the user choose these when instantiating
#  a client class.
BUFFER_SIZE = 1024
TIMEOUT = 3 # seconds

class Client:
    """A remote_object Client.

    This class allows a use to check attributes and make method calls
    on a python object hosted by the server.Server class. This is
    achieved by making a method call on the client.Client instance,
    which is then forwarded over the TCP socket to the server, which
    actually makes the requested method call and passes any return
    values or Exceptions back to the client to be returned or raised
    respectively.

    :param __ip: A string holding the address of the server.Server
                    instance which the Client will call from.

    :param __port: An integer holding the port number of the server.Server
                    instance which the Client will call from

    :method __call_method: The private method which actually parses the
                            client-requested call, passes this to the
                            server and then returns/raises the result.
                            This is not intended to be directly used.

    :Note: The Client class treats attribute lookups like method calls,
            but without arguments. So if the server-hosted python object
            has an attribute "a" it can be check by the Client class as
            client.Client(...).a()

    Example Usage::

        _client = client.Client('some ip',9999)

        # Attempts to call ".a()" on server,
        #  may return a value or error, depending
        #  on the hosted object
        print(_client.a())

        # Same as above
        print(_client.__getattr__("a")())

        # Raises AttributeError, since the client.Client
        #  class does not have a natuarl method "a"
        print(_client.__getattribute__("a")())
    """
    def __init__(self,ip,port):
        self.__ip,self.__port = ip,port

    def __repr__(self):
        try:
            _repr = self.__call_method("__repr__")
        except:
            _repr = "pointed at {0}:{1}".format(self.__ip,self.__port)
        return "<Remote Wrapper {}>".format(_repr)

    def __call_method(self,fname,*args,**kwargs):
        """Handler for method calls and returns

        This method takes a
        """
        socket = MessageSocket(self.__ip,self.__port)
        rmsg = socket.send_message(pickle.dumps((fname,args,kwargs)))
        socket.close()
        return_value = pickle.loads(rmsg)
        if isinstance(return_value, Exception):
            # If the server raised an error, reraise it here.
            #  In that case, return_values is an error.TraceableError
            #  type, hence it is called during reraising so as to print
            #  the server traceback
            error = return_value()
            # Using mixin_error allows any try ... except .... statments to
            #  catch either from `error.__class__` OR from `ro.errors.CallMethodError`
            raise mixin_error(error,"Remote Method Call Failed") from error
        return return_value

    def __getattr__(self,key):
        def f(*args,**kwargs):
            return self.__call_method(key,*args,**kwargs)
        return f

class MessageSocket(socket.socket):
    """A TCP socket wrapper for use by a remote_object.client.Client instance

    This class inherits from the base socket.socket class, see that
    documentation for details on the TCP socket connection. The
    main extension of this class is implement a single method to
    both send and receive a message, since when functioning properly,
    the server should always send a single response for the single message
    recieved from a socket. After this exchange, the socket is no longer
    used, and can be deleted.
    """
    def __init__(self,ip,port):
        socket.socket.__init__(self,socket.AF_INET,
                               socket.SOCK_STREAM)
        self.settimeout(TIMEOUT)
        self.connect((ip,port))

    def send_message(self,msg):
        """Sends a message, waits and returns the response

        :param msg: a bytes type containing the messasge to
                    be send (note, do NOT include a term char)

        :return rmsg: a bytes type containing the response
                        to the message (note, does NOT include
                        a term char)
        """
        self.sendall(msg + b'\n')
        self.buffer = b''
        while True:
            rmsg = self.recv(BUFFER_SIZE)
            if rmsg == b'':
                break
            self.buffer = self.buffer + rmsg
        return self.buffer.strip()
