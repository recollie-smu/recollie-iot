from microbit import *
import radio

radio.on()

def on_button_pressed_a():
    display.show(Image(
        "01010:"
        "00000:"
        "02020:"
        "00000:"
        "01010"))

    sleep(100)
    display.clear()

button_a.was_pressed(on_button_pressed_a)

def on_button_pressed_b():
    display.show(Image(
        "00200:"
        "02220:"
        "20202:"
        "21212:"
        "20102"))

    radio.send("ggggg22222")
    radio.send("mmmmm33333")
    radio.send("rrrrr55555")

    display.clear()

button_b.was_pressed(on_button_pressed_b)

while True:
    incoming = radio.receive()
    if incoming:
        display.show(incoming)
        sleep(100)
        display.clear()
