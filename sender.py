def on_button_pressed_a():
    radio.send_string("R1:0:N")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    basic.clear_screen()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_received_string(receivedString):
    room = receivedString.slice(0, 2)
    reminder = receivedString.slice(3, 4)
    if room == "R1":
        basic.show_string(receivedString)
radio.on_received_string(on_received_string)

def on_button_pressed_b():
    radio.send_string("R1:1:N")
input.on_button_pressed(Button.B, on_button_pressed_b)

radio.set_group(1)