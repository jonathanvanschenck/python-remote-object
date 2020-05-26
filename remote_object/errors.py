# TODO:
#     - Add error logging to TraceableError for server-side and error logging
#         for client-side which are better than just a 'print'
#     - Change TraceableError to actually inhert from error, and just override
#         whatever happens when raise gets called.

import traceback

class CallMethodError(Exception):
    """Exception to raise on client when server has error.
    """
    pass

class TraceableError(Exception):
    """Exception wrapper which saves the traceback for pickling

    This class is intended to allow the text of error tracebacks
    to be pickled and then printed when the unpickled error is
    raised. This is currently handled by calling the TraceableError
    instance when the error is intended to be reraised (after unpickling).

    :param error: An instance of some Exception type. The instance must
                    have a valid .__traceback__ attribute at the time of
                    instantiation for the TraceableError class. (which
                    should always be true of an Exception instance caught
                    by 'except Exception as e:')

    :param traceback: A string representation of the text of the traceback,
                        as it would have been printed into a terminal if
                        .error (at the time of initizalization of the class)
                        was raised.

    Example Usage::

        import pickle

        def a():
            return b()

        def b():
            raise Exception("Failures Abound!")

        try:
            a()
        except Exception as e:
            E = e
            E_trace = errors.TraceableError(e)

        # still retains some traceback info
        raise pickle.loads(pickle.dumps(E_trace()))

        # does not retain traceback info
        raise pickle.loads(pickle.dumps(E))
    """
    def __init__(self,error):
        self.error = error
        self.traceback = "\n".join(traceback.format_tb(error.__traceback__))
        print(self.traceback)

    def __call__(self):
        print("Traceback (From server):\n\n",self.traceback)
        return self.error
