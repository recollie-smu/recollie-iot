# this is in makeCode!!!
message = ""

def on_button_pressed_a():
    basic.show_leds("""
        . # . # .
                . . . . .
                . . # . .
                . . . . .
                . # . # .
    """)
    basic.pause(100)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    basic.show_leds("""
        . . # # #
                . . # . #
                # . # . #
                # . # . .
                # # # . .
    """)
    serial.write_line("ggggg22222")
    serial.write_line("mmmmm33333")
    serial.write_line("rrrrr55555")
    basic.clear_screen()
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_data_received():
    global message
    basic.show_leds("""
        # . # . .
                . . . . .
                # # # . .
                . . . . .
                . . . . .
    """)
    message = serial.read_line()
    basic.show_string(message)
    basic.pause(100)
    basic.clear_screen()
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)
