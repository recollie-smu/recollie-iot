def on_button_pressed_a():
    global val
    val = 0
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    radio.send_value("stop", 3)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global val
    val = 0
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    radio.send_value("stop", 3)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_received_string(receivedString):
    global val
    room = receivedString.slice(0, 1)
    reminder = receivedString.slice(2, 3)
    overdue = receivedString.slice(4, 5)
    if overdue == "Y":
        val = 2
    if room == "1":
        if reminder == "1":
            basic.show_icon(IconNames.GIRAFFE)
            music.play_melody("C - D E - C E - ", 120)
            music.play_melody("C E - D - E F F ", 120)
            music.play_melody("E D F - - - - - ", 120)
            basic.pause(2000)
            val = 1
radio.on_received_string(on_received_string)

val = 0
radio.set_group(1)

def on_forever():
    if val == 1:
        basic.show_leds("""
            . . . . .
                        . . . . .
                        . . # . .
                        . . . . .
                        . . . . .
        """)
        basic.pause(500)
        basic.show_leds("""
            . . . . .
                        . # # # .
                        . # . # .
                        . # # # .
                        . . . . .
        """)
        basic.pause(500)
        basic.show_leds("""
            . # # # .
                        # . . . #
                        # . . . #
                        # . . . #
                        . # # # .
        """)
        basic.pause(500)
basic.forever(on_forever)
