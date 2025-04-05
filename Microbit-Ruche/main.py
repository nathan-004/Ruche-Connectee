def get_state(pin: number):
    # Humidite + température
    return pins.analog_read_pin(pin)

def get_date():
    ms = input.running_time()
    # Modifier saison
    return [0, 0, 0, 0, 0]

# Envoyer signal avec le réseau LoRaWAN
def envoyer_message():
    pass


first_date = (4, 5, 9, 16, 0) # m, j, h, m, s

saisons = ["hiver",
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
]

saison = saisons[first_date[0] + 1]

def on_forever():
    date = get_date()
    temp = get_state(AnalogPin.P0)
    hum = get_state(AnalogPin.P1)
    # ----------------------------------Mettre nom du pin
    if saison == "automne" or saison == "hiver":
        if temp <= 0:
            # Modifier valeur
            envoyer_message()
        if hum >= 65:
            envoyer_message()
    else:
        if temp <= 0:
            envoyer_message()
        if hum >= 80:
            envoyer_message()

basic.forever(on_forever)
