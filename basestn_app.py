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

def microbit_data_logic():
    # TODO: WRITE WAYS TO HANDLE DATA FROM MICROBIT LOGIC HERE
    pass

def main():
    # Find the serial port for the micro:bit
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port.description)

    ser = connect2serial("COM5")

    # Wait for the micro:bit to initialize
    time.sleep(2)
    print("...connected to microbit!")

    isWriting = False
    # Read and write to microbit
    while True:
        # checks for api calls
        message = api_calls()
        if message != "":
            isWriting = True

        # Write to microbit if there is a command from API
        if isWriting:
            ser.write(message.encode())
            isWriting = False
        
        # Check if there is any data waiting in the serial buffer
        if ser.inWaiting() > 0:
            data = ser.readline().decode().rstrip()
            microbit_data_logic()
            print(data) # TO BE REMOVED

if __name__ == "__main__":
    main()


