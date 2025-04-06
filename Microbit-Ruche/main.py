def list(iterable):
    t = []
    
    for el in iterable:
        t.append(el)

    return t

def round(n):
    # Round to the lowest integer

    N = str(n)
    N1 = list(N)

    if "." not in N1:
        return n

    return int(N[:N1.index_of(".")])

def enumerate(iterable):
    return [(i, iterable[i]) for i in range(len(iterable))]

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
    return round(t)

def get_date():
    ms = input.running_time() # Nombre de ms depuis le lancement du programme
    date = []

    j = 0
    for i in range(4, -1, -1):
        date.append(convert(ms, 0, i))
        ms -= convert(date[j], i, 0)
        j+=1

    # Addition de first_date et de date
    max_ = [1000, 60, 60, 24, 30, 12]
    new_date = []

    for t in enumerate(date):
        idx, val = t
        res = val + first_date[idx]
        if res > max_[idx]:
            res %= max_[idx]
        new_date.append(res)

    if new_date[0] != first_date[0]:
        saison = saisons[date[0] - 1]

    return new_date

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
    serial.write_numbers(date)
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
