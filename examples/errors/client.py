from remote_object.client import Client
from remote_object.errors import CallMethodError

HOST, PORT = 'localhost', 9999

client = Client(HOST, PORT)

if __name__ == "__main__":
    print(client) # prints: <Remote Wrapper <Generic Python Object>>
    try:
        client.index_error()
    except IndexError:
        print("Index Error Caught")

    try:
        client.index_error()
    except CallMethodError:
        print("Index Error Caught as a Call Method Error")

    try:
        client.custom_error()
    except CallMethodError:
        print("Custom Error Caught as a Call Method Error")
