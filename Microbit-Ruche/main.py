def get_state(pin: number):
    # Humidite + température
    return pins.analog_read_pin(pin)

def convert(t, cur, res): # indexs
    calc = [1000, 60, 60, 24, 30] # ms -> s -> m -> h -> j
    if cur > res:
        for i in range(cur-1, res-1, -1):
            t *= calc[i]
    elif cur < res:
        for i in range(cur, res, 1):
            t /= calc[i]
    return t

def get_date():
    ms = input.running_time() # Nombre de ms depuis le lancement du programme

    date = []

    for i in range(4, -1, -1):
        date.append(convert(ms, 0, i))
        ms -= convert(date[-1], i, 0)

    if date[0] != first_date[0]:
        saison = saisons[date[0] - 1]

    return date


def envoyer_message(): # Envoyer signal avec le réseau LoRaWAN
    pass

first_date = [4, 5, 9, 16, 0] # m, j, h, m, s

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

saison = saisons[first_date[0] - 1]

def on_forever():
    date = get_date()
    temp = get_state(AnalogPin.P0)
    hum = get_state(AnalogPin.P1) # ----------------------------------Mettre nom du pin
    if saison == "automne" or saison == "hiver":
        if temp <= 0: # Modifier valeur
            envoyer_message()
        if hum >= 65:
            envoyer_message()
    else:
        if temp <= 0: # Modifier valeur
            envoyer_message()
        if hum >= 80:
            envoyer_message()

basic.forever(on_forever)
