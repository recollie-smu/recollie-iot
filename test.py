import socketio
import serial.tools.list_ports
import time
# Create a Socket.io client instance
sio = socketio.Client()

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.description)

# Open a serial port to listen for incoming data
ser = serial.Serial('COM5', 115200)
# Wait for the micro:bit to initialize
time.sleep(2)
print("...connected to microbit!")

@sio.event
def connect():
    print('Socket.io client connected')

@sio.event
def disconnect():
    print('Socket.io client disconnected')

@sio.on('socketio-event')
def on_socketio_event(data):
    print(f'Received Socket.io event: {data}')

# Connect the Socket.io client to the server
sio.connect('http://localhost:3000')

# Listen for incoming data from the serial port and Socket.io server
while True:
    # Check for incoming serial data
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        print(f'Received serial data: {data}')
        
        # Emit a Socket.io event with the serial data
        sio.emit('serial-data', data)

    # Listen for incoming Socket.io events
    sio.sleep(0.1)


# Wait for the client to disconnect
sio.wait()