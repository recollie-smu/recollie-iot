import serial.tools.list_ports
from time import localtime, strftime, sleep
import socketio

# TODO: put your own serial interface
SERIAL_INTERFACE = "COM5"
SERIAL_LOOPER_NAMESPACE = '/serial-looper'
LOCATION_DIR  = {1: 'r1', 2: 'r2', 3: 'r3', 4:'r4'}
TASKID_COLLECTION = {}

def connect_to_serial(serial_port: str):
    """Trys to connect to serial port"""
    try:
        print("Trying to connect to serial port: " + serial_port)
        return serial.Serial(serial_port, 115200)
    except:
        print("Connection failure! Closing ...")
        exit()

def process_microbit_raw_data(data: str):
    """Receive data from the microbit and process them to send to UI"""
    processed = ""

    # remove duplicated characters
    for characters in data:
        if characters in processed:
            continue
        processed += characters

    if is_data_corrupted(processed):
        print("Data received from serial is corrupted")
        return ""
    
    return processed

def is_data_corrupted(data: str):
    """Checks whether the data from microbit via serial is corrupted"""
    if len(data) != 2:
        return True
    
    if not data[1].isnumeric():
        return True
    
    return False

def send_to_socket_server(sio, data: str):
    """
    Receive data in the form of xy, where x is a letter in [g,r] only 
    and y is a number from 0 to 4 only
    """
    # TODO: WRITE INSTRUCTIONS TO UI

    op_code = data[0]
    index = data[1]
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

    if op_code == 'g':
        sendingObj = {
            'inputType': index, 
            'timestamp': timestamp
            }
        
        # Emit a Socket.io event with the serial data
        sio.emit('sensor', sendingObj, namespace=SERIAL_LOOPER_NAMESPACE)
        print(f'Sending to server : {sendingObj}')

    elif op_code == 'r':
         # TODO: change when josh decides
        try:
            sendingObj = {
                'taskId': TASKID_COLLECTION[index].pop(0),
                'status': 3,
                'location': index
                }
        except KeyError:
            print('Task id not in buffer')
        
        # Emit a Socket.io event with the serial data
        sio.emit('task', sendingObj, namespace=SERIAL_LOOPER_NAMESPACE)
        print(f'Sending to server : {sendingObj}')

    else:
        print('Unrecognised op code')

def process_ui_raw_data(data):
    """Receive data from the UI and process them to send to microbit"""
    try:
        task_id = data['taskId']
        status = data['status']
        location = LOCATION_DIR[data['location']]
    except KeyError:
        print('Format from UI is not accepted')
        return ''
    
    # TODO: check way of buffer
    if TASKID_COLLECTION.get(data['location']) is None:
        TASKID_COLLECTION[data['location']] = [task_id]
    else:
        TASKID_COLLECTION[data['location']].append(task_id)

    return f'{location}:{status}\n'

def main():

    # Find the serial port for the micro:bit
    # code not working for now
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port.description)

    ser = connect_to_serial("COM5")
    # Wait for the micro:bit to initialize
    sleep(2)
    print("...connected to microbit!")
    
    sio = socketio.Client()

    @sio.on('connect', namespace=SERIAL_LOOPER_NAMESPACE)
    def on_connect():
        print(f"Connected to server as namespace='{SERIAL_LOOPER_NAMESPACE}'")

    # Receiving task
    @sio.on('task', namespace=SERIAL_LOOPER_NAMESPACE)
    def on_task(data):
        print(f'Received from server : {data}')
        processed = process_ui_raw_data(data)
        if not processed == '':
            ser.write(processed.encode())

    # Connect to the server
    sio.connect('http://localhost:8080',namespaces=[SERIAL_LOOPER_NAMESPACE])
    
    # Read and write to microbit
    while True:        
        # Check if there is any data waiting in the serial buffer
        if ser.inWaiting() > 0:
            data = ser.readline().decode().rstrip()
            op_code = process_microbit_raw_data(data)
            if op_code == '':
                continue
            send_to_socket_server(sio, op_code)

if __name__ == "__main__":
    main()


