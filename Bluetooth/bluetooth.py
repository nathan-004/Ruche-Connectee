def on_uart_data_received():
    received = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    serial.write_line(received)

bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),on_uart_data_received)

bluetooth.start_uart_service()
basic.show_icon(IconNames.HAPPY)
