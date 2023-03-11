def on_button_pressed_a():
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    radio.send_string("" + ("rrr:111\n"))
    basic.pause(2000)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_received_string(receivedString):
    room = receivedString.slice(0, 1)
    reminder = receivedString.slice(2, 3)
    overdue = receivedString.slice(4, 5)
    if overdue == "Y":
        basic.show_icon(IconNames.ANGRY)
    if room == "1":
        if reminder == "1":
            basic.show_icon(IconNames.HEART)
            music.play_melody("C - D E - C E - ", 120)
            music.play_melody("C E - D - E F F ", 120)
            music.play_melody("E D F - - - - - ", 120)
radio.on_received_string(on_received_string)

def on_button_pressed_b():
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    radio.send_string("" + ("rrrr1111\n"))
    basic.pause(2000)
    basic.clear_screen()
input.on_button_pressed(Button.B, on_button_pressed_b)

radio.set_group(1)