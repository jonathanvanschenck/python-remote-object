"""

TODO:
    - Add error logging to TraceableError for server-side and error logging
        for client-sdie which are better than just a 'print' 
"""

import traceback

class CallMethodError(Exception):
    def __init__(self,message=""):
        self.message = message
        
        
class TraceableError(Exception):
    def __init__(self,error):
        self.error = error
#        error.__traceback__
#        traceback.print_tb(error.__traceback__)
        self.traceback = "\n".join(traceback.format_tb(error.__traceback__))
        print(self.traceback)
        
    def __call__(self):
        print("Traceback (From server):\n\n",self.traceback)
        return self.error#.with_traceback(self.traceback)