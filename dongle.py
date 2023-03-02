def on_received_value(name, value):
    serial.write_value(name, value)
    if value == 9:
        basic.show_number(1)
radio.on_received_value(on_received_value)

def on_data_received():
    global line, key, val, followed
    # toggle an LED to show that some data is being received
    led.toggle(2, 2)
    # line should be either "f:0", "f:1", "i:0", or "i:0"
    line = serial.read_until(serial.delimiters(Delimiters.CARRIAGE_RETURN))
    # is it possible to use split(":") instead? Try using split() then convert to blocks and see what happens
    key = line[0]
    val = parse_float(line[2])
    if key == "f":
        followed = val
    elif key == "i":
        # Show an icon or clear the screen depending on the value of val
        if val == 1:
            basic.show_icon(IconNames.HEART)
            soundExpression.hello.play()
            radio.send_string(serial.read_until(serial.delimiters(Delimiters.CARRIAGE_RETURN)))
        elif val == 0:
            basic.show_icon(IconNames.STICK_FIGURE)
            soundExpression.happy.play()
            radio.send_string(serial.read_until(serial.delimiters(Delimiters.CARRIAGE_RETURN)))
        elif val == 3:
            basic.show_icon(IconNames.YES)
            soundExpression.yawn.play()
            radio.send_string(serial.read_until(serial.delimiters(Delimiters.CARRIAGE_RETURN)))
        elif val == 2:
            basic.show_icon(IconNames.PITCHFORK)
            soundExpression.slide.play()
            radio.send_string(serial.read_until(serial.delimiters(Delimiters.CARRIAGE_RETURN)))
serial.on_data_received(serial.delimiters(Delimiters.CARRIAGE_RETURN),
    on_data_received)

followed = 0
val = 0
key = ""
line = ""
basic.clear_screen()
# Write the device name to the serial port. By pressing the reset button on the micro:bit, the device name will be displayed on the laptop. This helps with debugging, to ensure that the serial port is working
serial.write_line(control.device_name())
radio.set_group(0)
# Every 2 seconds, if the followed variable is set to 1, then send a sensor reading to the serial port

def on_forever():
    if followed == 1:
        serial.write_value("a_x", input.acceleration(Dimension.X))
    basic.pause(2000)
basic.forever(on_forever)