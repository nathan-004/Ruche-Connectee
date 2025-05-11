message = ""

def on_bluetooth_connected():
    bluetooth.start_uart_service()
    basic.show_string("C")
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_string("D")
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_uart_data_received():
    global message
    message = bluetooth.uart_read_until(serial.delimiters(Delimiters.HASH))
    bluetooth.uart_write_string(message)
    basic.show_string(message)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.HASH), on_uart_data_received)
