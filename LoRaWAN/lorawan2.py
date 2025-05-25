from microbit import *

class BaudRate():
    BAUD_RATE9600 = 9600
    BAUD_RATE14400 = 14400
    BAUD_RATE19200 = 19200
    BAUD_RATE38400 = 38400
    BAUD_RATE57600 = 57600
    BAUD_RATE115200 = 115200
    BAUD_RATE128000 = 128000
    BAUD_RATE256000 = 256000

class LoRaWan():

    DEFAULT_TRANSMITTER = pin14
    DEFAULT_RECEIVER = pin0
    DEFAULT_BAUDRATE = 9600
    END = "\r\n"
    DEFAULT_TIMEOUT = 5000

    def __init__(self, baudrate:int = 9600, tx=None, rx=None):
        if tx is None:
            tx = self.DEFAULT_TRANSMITTER
        elif rx is None:
            rx = self.DEFAULT_RECEIVER

        self.tx = tx
        self.rx = rx
        self.baudrate = baudrate

        uart.init(baudrate=baudrate, tx=tx, rx=rx)

    def send_command(self, cmd:str, timeout = None):
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        new_cmd = cmd + self.END
        uart.write(new_cmd)
        response = self.check_response(timeout)
        return response

    def check_response(self, timeout:int=5000):
        t = round(timeout / 100)
        val = "Pas de réponse"
        for i in range(100):
            if uart.any():
                val = uart.read()
                break
            sleep(t)
        return val

lora = LoRaWan(baudrate=BaudRate.BAUD_RATE115200)
val = lora.send_command("AT", timeout=10000)

uart.init(115200)
uart.write(str(val) + "\n")
display.scroll(str(val))
