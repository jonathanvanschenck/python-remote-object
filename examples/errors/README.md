# Errors
This example is intended to show how to catch errors with the `python-remote-object`
package.

## How it works
### The `TraceableError` Wrapper
All errors which happen on the server (as part of a method call) are forwarded
to the client, but not in their original form. First, the error is wrapped with
in a `remote_object.errors.TraceableError` object, which saves the traceback
as a string (since trackback attribute native to the error is lost during
serialization).
### Why `cloudpickle`?
Next, the wrapped object is serialized using the `cloudpickle` library. This is
has to do with how the base `pickle` library serializes user-defined (or simply
none-standard) exceptions and classes. Suppose the server used the base `pickle`
library to serialize a custom error. When the client tries to deserialize it later,
the custom error must have been manually imported into the module where the client
is attempting the deserialization, otherwise `pickle.loads` will throw an `AttributeError`
(like: `AttributeError: Can't get attribute 'CustomError' on <module '__main__' from 'client.py'>`),
since it can't find the source code to construct the custom error object.
On the other hand, the `cloudpickle` library is specifically designed to pickle
objects so that later depickling doesn't require direct access to the object
source code.
This instances where this problem arise are small, but it prevents obscure bugs.
### The Error Mixin
After the `remote_object.errors.TraceableError` object is serialized and sent to
the client, the object is deserialized and called (which prints the traceback
and returns the error instance). Then, a new error type is created with inherits
from from both the deserialized error class type AND the custom error type
`remote_object.errors.CallMethodError`. This new hybrid error is then raised
by the client. The reason for this is to standardize error handling on the client
side. Because the client might not necessarily have access to all the custom
error types which the server can throw (all the more reason to use `cloudpickle`),
and also because the client might simply want to catch all (but only) the errors
coming from the server, it is useful to have the `CallMethodError` type mixed in
to the error which is raised on the client. In this way:
```python3
client_object = remote_object.client.Client(HOST,PORT)
try:
  client_object.method_which_raises_an_exception()
except CallMethodError:
  print("I catch and (and only) server-side errors")
except Exception:
  print("I catch everything else")
```
At the same time, if the client does have access to the types of errors which
the server is expected to throw, it is advantageous to be able to handle errors
in the standard way:
```python3
client_object = remote_object.client.Client(HOST,PORT)
try:
  client_object.method_which_raises_an_IndexError()
except AttributeError:
  print("I don't catch this")
except IndexError:
  print("I do catch this")
except CallMethodError:
  print("I'll catch everything else")
```

## See it in action
In one terminal, run
```bash
 $ python3 server.py
```
In another terminal run
```bash
 $ python3 client.py
```
