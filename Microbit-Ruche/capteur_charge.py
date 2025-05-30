from microbit import *

CLK = pin0    # connecté à SCK
DATA = pin14  # connecté à DOUT

def read_hx711():
    count = 0
    while DATA.read_digital() == 1:
        sleep(1)

    for i in range(24):
        CLK.write_digital(1)
        count = count << 1
        CLK.write_digital(0)
        if DATA.read_digital():
            count += 1

    CLK.write_digital(1)
    CLK.write_digital(0)

    if count & 0x800000:
        count |= ~0xffffff
    return count

while True:
    valeur = read_hx711()
    uart.write(str(valeur))
    sleep(2000)
