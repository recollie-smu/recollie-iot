def on_gesture_down():
    serial.write_string("" + ("gggg2222\n"))
    basic.show_icon(IconNames.HAPPY)
    basic.pause(5000)
    basic.clear_screen()
grove.on_gesture(GroveGesture.DOWN, on_gesture_down)

def on_gesture_right():
    serial.write_string("" + ("gggg1111\n"))
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

def on_received_string(receivedString):
    serial.write_string(receivedString)
radio.on_received_string(on_received_string)

def on_data_received():
    radio.send_string(serial.read_line())
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

radio.set_group(1)

def on_forever():
    if pins.analog_read_pin(AnalogPin.P0) == 1012:
        serial.write_string("" + ("mmmm1111\n"))
    basic.pause(1000)
basic.forever(on_forever)
