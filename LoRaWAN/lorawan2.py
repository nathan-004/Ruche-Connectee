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
        return str(response)

    def check_response(self, timeout:int=5000):
        t = round(timeout / 100)
        val = "Pas de réponse"
        for i in range(100):
            if uart.any():
                val = uart.read()
                break
            sleep(t)
        return val

    def display_result(self, string:str):
        """Affiche une chaîne de charactères via UART"""
        uart.init(BaudRate.BAUD_RATE115200)
        uart.write(string + "\n")
        uart.init(self.baudrate, tx=self.tx, rx=self.rx)
        
    def show_IDs(self, timeout = None):
        """Envoie une commande AT pour montrer les IDENTIFIANTS de l'appareil"""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        dev_eui = self.send_command("AT+ID=DevEui", timeout)
        app_eui = self.send_command("AT+ID=AppEui", timeout)
        self.display_result(dev_eui)
        self.display_result(app_eui)

    def wake_up(self):
        """Set the Low Power mode to  AUTOOFF"""
        wakeup = bytes([0xFF, 0xFF, 0xFF, 0xFF])
        cmd = b"AT+LOWPOWER=AUTOOFF\r\n"

        uart.write(wakeup + cmd)

        return self.check_response()

lora = LoRaWan(baudrate=BaudRate.BAUD_RATE115200)
val = lora.wake_up()

uart.init(115200)
uart.write(str(val) + "\n")
display.scroll(str(val))
