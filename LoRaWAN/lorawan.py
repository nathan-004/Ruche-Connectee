from microbit import *
import time

# Utilisation de l'UART pour communiquer avec le module Wio-E5
uart.init(baudrate=9600, bits=8, parity=None, stop=1)

# Infos TTN (à modifier avec les vôtres)
DevEUI = "XXXXXXXXXXXXXXXX"
AppEUI = "YYYYYYYYYYYYYYYY"
AppKey = "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"

# Fonction pour envoyer une commande AT et attendre la réponse
def send_at(cmd, delay=2000):
    uart.write((cmd + '\r\n'))
    time.sleep_ms(delay)
    response = uart.read()
    if response:
        print(response.decode('utf-8'))
    else:
        print("Pas de réponse.")

# Initialisation LoRa
def init_lora():
    display.show('I')  # Init
    send_at('AT+ID=DevEUI,"{}"'.format(DevEUI))
    send_at('AT+ID=AppEUI,"{}"'.format(AppEUI))
    send_at('AT+KEY=APPKEY,"{}"'.format(AppKey))
    send_at('AT+DR=EU868')  # Région
    send_at('AT+MODE=LWOTAA')  # Activation via OTAA
    send_at('AT+JOIN')  # Rejoindre le réseau
    display.show('J')  # Join
    time.sleep(10)

# Envoi d’un message
def send_message(payload):
    # Envoyer en format hexadécimal
    send_at('AT+MSGHEX="{}"'.format(payload.encode('utf-8').hex()))

# Programme principal
init_lora()
display.show('S')  # Send

while True:
    # Exemple : envoyer "Hello"
    send_message("Hello")
    display.show(Image.HAPPY)
    sleep(60000)  # attendre 1 minute
