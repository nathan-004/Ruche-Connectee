from microbit import *
import serial

# Remplace par tes clés TTN
DevEUI  = "0123456789ABCDEF"
AppEUI  = "0011223344556677"
AppKey  = "AABBCCDDEEFF00112233445566778899"

# Rediriger l'UART sur P0 (TX) et P1 (RX) à 9600 bauds
serial.redirect(SerialPin.P0, SerialPin.P1, 9600)

# Envoie une commande AT et attend la réponse
def send_at(cmd):
    serial.write_string(cmd + "\r\n")
    basic.pause(2000)
    resp = serial.read()
    if resp:
        basic.show_string("R")   # Réponse reçue
    else:
        basic.show_string("E")   # Erreur / pas de réponse

# Initialisation du module Wio-E5 pour TTN
def init_lora():
    basic.show_string("I")  # Init
    send_at("AT")      # Test de vie
    send_at("AT+ID=DevEUI,\""  + DevEUI + "\"")
    send_at("AT+ID=AppEUI,\""  + AppEUI + "\"")
    send_at("AT+KEY=APPKEY,\"" + AppKey + "\"")
    send_at("AT+DR=EU868")
    send_at("AT+MODE=LWOTAA")
    send_at("AT+JOIN")
    basic.show_string("J")  # Join
    basic.pause(10000)

def char_to_hex(c):
    # Simuler ord() pour les lettres et chiffres de base
    alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    index = 0
    while index < len(alphabet):
        if alphabet[index] == c:
            ascii_code = index + 32  # car alphabet commence à l'ASCII 32 (espace)
            break
        index += 1

    hex_chars = "0123456789ABCDEF"
    high = ascii_code // 16
    low = ascii_code % 16
    return hex_chars[high] + hex_chars[low]

def send_message(text):
    hex_msg = ""
    for i in range(len(text)):
        c = text[i]
        hex_msg += char_to_hex(c)
    serial.write_string("AT+MSGHEX=\"" + hex_msg + "\"\r\n")

# Programme principal
init_lora()
basic.show_string("S")
while True:
    send_message("HELLO")  # envoie "HELLO"
    basic.show_icon(IconNames.HAPPY)
    basic.pause(60000)           # toutes les 60 secondes
