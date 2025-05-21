from microbit import *

uart.init(115200, tx=pin0, rx=pin14)

uart.write('AT\r\n')
response = "test"

for i in range(100):
    sleep(100)
    if uart.any():
        response = uart.readline()
        break
        
uart.init(115200)
uart.write(str(response))
uart.write("\n")
display.scroll(str(response))
