"""This is for testing purposes!"""
from multiprocessing.connection import Client

# WEBSOCKET_PASSWORD = b"Tyh56hg"
WEBSOCKET_PASSWORD = b"secret password"

address = ('localhost', 6000)
conn = Client(address, authkey=WEBSOCKET_PASSWORD)

endLoop = False
while not endLoop:
    
    inp = input('input:')

    if inp == 'close':
        conn.send(inp)
        endLoop = True

    conn.send(inp)
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()