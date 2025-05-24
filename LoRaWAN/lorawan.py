def on_data_received():
    rcvData = serial.read_until(serial.delimiters(Delimiters.NEW_LINE))
    basic.show_string(rcvData)
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

serial.redirect(tx=SerialPin.P14, rx=SerialPin.P0, rate=BaudRate.BAUD_RATE115200)

serial.write_string("AT" + "\r\n")
