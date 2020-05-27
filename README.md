# python-remote-object
Python TCP server and client which allows clients to make calls and get returns
from a python object instantiated on the server.

This package was originally developed to be used along side `pyUSB`, `serial`,
`pyVISA`, etc, where an external hardware component could be connected to a
computer for which a python-based API for the component already existed. This
package could then take an instance of that python driver, and allow other
computers (potentially off-site) to make API calls and so control the external
hardware remotely.

For example, one could connect a raspberry pi up to their digital oscilloscope
via usb, and now your oscilloscope is "wifi-enabled"

# Security Note
ONLY INTERACT WITH SERVERS THAT YOU TRUST. The `remote_object.client.Client`
object uses `pickle.load` to deserialize data and objects from the server. This
process is able to execute arbitrary code on your machine. This can easily be
exploited by malicious agents to compromise your system. The `pickle` library,
and by extension `python-remote-object`, leave it to the user to make wise
decisions about what they chose to unpickle. Be smart.

# Installation
## Pip
To get the current stable version, install using pip:
```bash
 $ pip3 install remote_object
```
## Development Version
To get the development version, clone this repo, then inside the folder create a `python3` virtual environment, activate it, and install using setuptools:
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
 (venv) $ python3 setup.py install
 ```

# Basic Use

If you have an instance of a python object, `pyobj`, using the base server
class `remote_object.server.Server` will allow you to create a TCP server
which hosts `pyobj`.

On the client end, you must create an instance of the `remote_object.client.Client`
object pointed at the server's address and port. By default, calling a method
on the `Client` instance will pass that call across the TCP connection to the
server, where the `Server` instance will make that method call on `pyobj`. Any
errors or return values will then be passed back to the `Client` instance and
raised or returned respectively.

For example, the server might look like:
```python
from remote_object.server import Server

HOST, PORT = 'your-ip-address', 9999

class Test:
    def __init__(self):
        self.a = "attribute a"

    def __repr__(self):
        return "<Test Class>"

    def b(self,message):
        return "method b: " + message

with Server((HOST, PORT),Test()) as server:
    server.serve_forever()

```
The client might then look like:
```python
from remote_object.server import Client

with Client(HOST, PORT) as client:
    print(client) # prints: <Remote Wrapper <Test Class>>    
    print(client.a()) # prints "attribute a"
    print(client.b("Hello!")) # prints "method b: Hello!"
    print(client.c()) # raises AttributeError
```

Note here that attributes are treated like methods without arguments, and
attempting to call method which does not exist will raise an `AttributeError`.

See `examples/errors` for additional info.

# Development
For development, clone this directory, then have fun! Pro-tip: setup a python
virtual environment in the main directory:
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
```
## Installing
```bash
 (venv) $ python3 setup.py install
```

## Creating source packages
```bash
 (venv) $ python3 setup.py sdist bdist_wheel
```

## Uploading to PyPI
```bash
 (venv) $ python3 -m twine upload dist/*
```

See: [https://packaging.python.org/tutorials/packaging-projects/]
