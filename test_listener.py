"""This is for testing purposes!"""

from multiprocessing.connection import Listener
from multiprocessing.context import AuthenticationError
import time

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
print(2)
listener = Listener(address, authkey=b'secret password')
print(5)
conn = ''
try:    
    conn = listener.accept()
except :
    print('error')
    exit()
    
print('connection accepted from', listener.last_accepted)
while True:
    msg = ''
    cond = conn.poll()
    # do something with msg
    if cond:
        msg = conn.recv()
        print("msg: ", msg)

    time.sleep(3)
    print('ff')

    if msg == 'close':
        conn.close()
        break
listener.close()