import eventlet
import socketio
import serial

# Create a Socket.IO server instance
sio = socketio.Server()

@sio.event
def connect(sid, environ):
    print(f'environ: {environ}')
    print(f'Socket.IO client {sid} connected')

@sio.event
def disconnect(sid):
    print(f'Socket.IO client {sid} disconnected')

@sio.on('print-to-console')
def print_to_console(sid, data):
    print(f'Received input from {sid}: {data}')

@sio.on('socketio-event')
def on_socketio_event(data):
    print(f'Received Socket.io event: {data}')

@sio.on('message')
def on_socketio_event(data):
    print(f'Received message: {data}')

# Start the Socket.IO server
app = socketio.WSGIApp(sio)
eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)
