from microbit import *

class LoRaWan():

    DEFAULT_TRANSMITTER = pin14
    DEFAULT_RECEIVER = pin0
    DEFAULT_BAUDRATE = 9600
    END = "\r\n"

    def __init__(self, baudrate:int = 9600, tx=None, rx=None):
        if tx is None:
            tx = self.DEFAULT_TRANSMITTER
        elif rx is None:
            rx = self.DEFAULT_RECEIVER

        self.tx = tx
        self.rx = rx
        self.baudrate = baudrate

        uart.init(baudrate=baudrate, tx=tx, rx=rx)

    def send_command(self, cmd:str):
        new_cmd = cmd + self.END
        uart.write(new_cmd)
        response = self.check_response()
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

lora = LoRaWan()
val = lora.send_command("AT")

uart.init(115200)
uart.write(str(val) + "\n")
display.scroll(str(val))
