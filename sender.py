def on_gesture_right():
    serial.write_string("" + ("gggg2222\n"))
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    basic.pause(5000)
    basic.clear_screen()
grove.on_gesture(GroveGesture.RIGHT, on_gesture_right)

def on_gesture_left():
    serial.write_string("" + ("gggg3333\n"))
    basic.show_icon(IconNames.HAPPY)
    basic.pause(5000)
    basic.clear_screen()
grove.on_gesture(GroveGesture.LEFT, on_gesture_left)

def on_received_string(receivedString):
    serial.write_string(receivedString)
radio.on_received_string(on_received_string)

def on_data_received():
    radio.send_string(serial.read_line())
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

radio.set_group(1)

def on_forever():
    if pins.analog_read_pin(AnalogPin.P0) > 1000:
        serial.write_string("" + ("gggg1111\n"))
    basic.pause(5000)
basic.forever(on_forever)
