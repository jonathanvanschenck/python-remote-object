'''Test the latency time of a Server/Client connection

Run this script in two different terminals:
    1) python simple_class.py server
    2) python simple_class.py client
'''

from sys import argv
import time
import numpy as np
from python_remote_object.server import Server
from python_remote_object.client import Client

HOST, PORT = 'localhost', 9999
N = 100

if __name__ == "__main__" and argv[1] == "server":
    with Server((HOST, PORT), time) as server:
        print("Hosting at: {0}|{1}".format(HOST,PORT))
        server.serve_forever()
      
elif __name__ == "__main__" and argv[1] == "client":
    client = Client(HOST, PORT)
    print(client,"\n")
    t = np.zeros(N+1)
    for IT in [1e-3,1e-2,5e-2,1e-1]:
        t[0] = time.time()
        for i in range(N):
            client.sleep(IT)
            t[i+1] = time.time()
        dt = 1e3*np.diff(t) # convert to ms
        print("Sleep time = {0:.0f} ms".format(IT*1e3))
        print("Total Method Call time = {0:.0f}+-{1:.1f} ms".format(np.mean(dt),np.std(dt)))
        print("Latency Time = {0:.0f}+-{1:.1f} ms ({2:.1%})".format(np.mean(dt)-IT*1e3,np.std(dt),1-IT*1e3/np.mean(dt)))
        print()
        
