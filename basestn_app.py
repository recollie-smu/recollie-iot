import serial.tools.list_ports
import time

def connect2serial(serial_port):
    """Trys to connect to serial port"""
    try:
        return serial.Serial(serial_port, 115200)
    except:
        print("Connection failure! Closing ...")
        exit()

def api_calls():
    """Checks for any API calls and returns them in a alphabet and number pair else returns an empty string"""
    # TODO: WRITE API CALLS HERE
    return ""
    return "ttttt99999"

def writing2ui(op_code):
    # TODO: WRITE DATA TO UI
    pass

def microbit_data_logic():
    """Receive data from the microbit and process them to send to UI"""

    

def main():
    # Find the serial port for the micro:bit
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port.description)

    ser = connect2serial("COM5")

    # Wait for the micro:bit to initialize
    time.sleep(2)
    print("...connected to microbit!")

    is_writing = False
    # Read and write to microbit
    while True:
        # checks for api calls
        message = api_calls()
        if message != "":
            is_writing = True

        # Write to microbit if there is a command from API
        if is_writing:
            ser.write(message.encode())
            is_writing = False
        
        # Check if there is any data waiting in the serial buffer
        if ser.inWaiting() > 0:
            data = ser.readline().decode().rstrip()
            op_code = microbit_data_logic()

            print(data) # TO BE REMOVED

if __name__ == "__main__":
    main()


