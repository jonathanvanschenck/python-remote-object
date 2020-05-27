from remote_object.server import Server

HOST, PORT = 'localhost', 9999

class CustomError(Exception):
    pass

class PythonObject:
    def __init__(self):
        pass

    def index_error(self):
        raise IndexError("Wrong index!")

    def custom_error(self):
        raise CustomError("Custom Error raised")

    def __repr__(self):
        return "<Generic Python Object>"



if __name__ == "__main__":
    with Server((HOST, PORT), PythonObject()) as server:
        print("Hosting at: {0}|{1}".format(HOST,PORT))
        server.serve_forever()
