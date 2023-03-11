import serial.tools.list_ports
import time
import requests

# TODO: put your own serial interface
SERIAL_INTERFACE = "COM5"
# TODO: Change url to API
API_URL = "https://www.w3schools.com/python/demopage.php"
OP_CODES = {'r': 'radio', 'g': 'gestures', 'm': 'motion'}

def connect2serial(serial_port: str):
    """Trys to connect to serial port"""
    try:
        print("Trying to connect to serial port: " + serial_port)
        return serial.Serial(serial_port, 115200)
    except:
        print("Connection failure! Closing ...")
        exit()

def api_calls():
    """Checks for any API calls and returns them in a alphabet and number pair else returns an empty string"""
    # TODO: WRITE API CALLS HERE REMEMBER TO END WITH \n !!!!!!!!!
    return ""
    # return "1234567\n"

def microbit_data_logic(data: str):
    """Receive data from the microbit and process them to send to UI"""
    processed = ""

    # remove duplicated characters
    for characters in data:
        if characters in processed:
            continue
        processed += characters
    
    if isDataCorrupted(processed):
        print("Data received from serial is corrupted")
        return ""
    
    return processed

def isDataCorrupted(data: str):
    """Checks whether the data from microbit via serial is corrupted 
    i.e. not in the form of xy, where x is a letter in [r,g,m] only 
    and y is a number from 0 to 4 only"""
    if len(data) != 2:
        return True
    
    if data[0] not in OP_CODES:
        return True
    
    if not data[1].isnumeric():
        return True
    
    return False

def postRequest2Api(data: str):
    """
    Receive data in the form of xy, where x is a letter in [r,g,m] only 
    and y is a number from 0 to 4 only
    """
    # TODO: WRITE INSTRUCTIONS TO UI

    op_code = OP_CODES[data[0]]
    index = data[1]

    sendingObj = {
        'operation': op_code, 
        'index': index
        }
    
    response = requests.post(API_URL, json = sendingObj)

    return response

def main():

    # Find the serial port for the micro:bit
    # code not working for now
    # ports = serial.tools.list_ports.comports()
    # for port in ports:
    #     print(port.description)

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
            op_code = microbit_data_logic(data)
            response = postRequest2Api(op_code)
            print(response) # e.g. <Response [200]>
            print(data) # TO BE REMOVED

if __name__ == "__main__":
    main()


