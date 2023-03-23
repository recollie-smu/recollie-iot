def on_button_pressed_a():
    global val
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    val = 0
    radio.send_string("" + ("rrrr3333\n"))
    basic.pause(2000)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_received_string(receivedString):
    global val
    room = receivedString.slice(0, 2)
    reminder = receivedString.slice(3, 4)
    if reminder == "2":
        basic.show_icon(IconNames.ANGRY)
        val = 1
    if room == "r3":
        if reminder == "1":
            basic.show_icon(IconNames.HEART)
            music.play_melody("C - D E - C E - ", 120)
            music.play_melody("C E - D - E F F ", 120)
            music.play_melody("E D F - - - - - ", 120)
radio.on_received_string(on_received_string)

def on_button_pressed_b():
    global val
    basic.show_leds("""
        . # . # .
                . . # . .
                . . # . .
                . . # . .
                . # . # .
    """)
    val = 0
    radio.send_string("" + ("rrrr3333\n"))
    basic.pause(2000)
    basic.clear_screen()
input.on_button_pressed(Button.B, on_button_pressed_b)

val = 0
voltage = 0
radio.set_group(1)

def on_forever():
    voltage = pins.analog_read_pin(AnalogPin.P0)
    if val == 1:
        music.start_melody(music.built_in_melody(Melodies.BADDY), MelodyOptions.ONCE)
    if voltage <= 256 and val == 0:
        radio.send_string("" + ("bbbb3333\n"))
basic.forever(on_forever)
