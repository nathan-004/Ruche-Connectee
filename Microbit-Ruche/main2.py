# Imports go at the top
from microbit import *
import log


R_HIGH = 1
R_MEDIUM = 2
R_LOW = 3

class SHT31:
    _map_cs_r = {
        True: {R_HIGH: b'\x2c\x06', R_MEDIUM: b'\x2c\x0d', R_LOW: b'\x2c\x10'},
        False: {R_HIGH: b'\x24\x00', R_MEDIUM: b'\x24\x0b', R_LOW: b'\x24\x16'}
    }

    def __init__(self, addr=0x44):
        i2c.init(freq=20000)  # Initialize I2C with 20kHz frequency
        self._addr = addr

    def _send(self, buf):
        i2c.write(self._addr, buf)

    def _recv(self, count):
        return i2c.read(self._addr, count)

    def _raw_temp_humi(self, r=R_HIGH, cs=True):
        if r not in (R_HIGH, R_MEDIUM, R_LOW):
            raise ValueError('Wrong repeatability value given!')
        self._send(self._map_cs_r[cs][r])  # Send command based on repeatability and clock stretching
        sleep(50)
        raw = self._recv(6)  # Receive 6 bytes of data (2 for temperature, 2 for humidity, 2 for checksum)
        return (raw[0] << 8) + raw[1], (raw[3] << 8) + raw[4]  # Unpack temperature and humidity data

    def get_temp_humi(self, data='t', resolution=R_HIGH, clk_stretch=True, celsius=True):
        t, h = self._raw_temp_humi(resolution, clk_stretch)  # Get raw temperature and humidity data
        sleep(50)  # Small delay before returning values
        if celsius:
            temp = -45 + (175 * (t / 65535))  # Convert to Celsius
        else:
            temp = -49 + (315 * (t / 65535))  # Convert to Fahrenheit
        if data == 't':  # Return temperature
            return temp
        elif data == 'h':  # Return humidity
            return 100 * (h / 65535)
        else:
            return None  # If data is neither 't' nor 'h', return None

# Create an SHT31 instance
sensor = SHT31()

def str_list(liste, sep=""):
    res = ""

    for el in liste:
        res += sep + str(el)

    return res[1:]

def copy(liste):
    t = []

    for el in liste:
        t.append(el)

    return t

FIRST_DATE = [0,29,23,59,59]
date = copy(FIRST_DATE) # m, j, h, m, s

saisons = ("hiver",
    "hiver",
    "hiver",
    "printemps",
    "printemps",
    "printemps",
    "ete",
    "ete",
    "ete",
    "automne",
    "automne",
    "automne"
)

saison = saisons[FIRST_DATE[0] - 1]

@run_every(s=1)
def modify_date():

    t = [12, 30, 24, 60, 60]
    date[-1] += 1
    
    for i in range(len(t)-1, -1, -1):
        if date[i] >= t[i]:
            if i != 0:
                date[i-1] += 1
                date[i] %= t[i]
            else:
                date[i] %= t[i]
    
    if date[0] != FIRST_DATE[0]:
        saison = saisons[date[0] - 1]

@run_every(min=15)
def send_data():
    temperature = sensor.get_temp_humi(data="t")
    humidity = sensor.get_temp_humi(data='h')
    
    datas = []

# Main loop
while True:
    # Get temperature and humidity
    temperature = sensor.get_temp_humi(data='t', resolution=R_HIGH)
    humidity = sensor.get_temp_humi(data='h', resolution=R_HIGH)
    
    # Display the temperature and humidity on the micro:bit
    display.scroll("T: {:.1f}C, H: {:.1f}%".format(temperature, humidity))
    
    sleep(2000)  # Wait for 2 seconds before refreshing the display
