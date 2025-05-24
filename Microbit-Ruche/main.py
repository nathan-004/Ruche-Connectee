import JSON

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

def len(iterable):
    i = 0
    for el in iterable:
        i+=1
    return i

def modify_parameters():
    global message

    # Message sous forme de JSON {"Intervalle": temps en min, "Seuil de temp": température, "Seuil de hum": humidité, "Current time": temps sous forme [mois, jour, heure, minute, secondes]}
    dictionnaire = JSON.parse(message)

    

message = ""

def on_bluetooth_connected():
    bluetooth.start_uart_service()
    basic.show_string("C")
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_string("D")
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_uart_data_received():
    global message
    message = bluetooth.uart_read_until(serial.delimiters(Delimiters.HASH))
    bluetooth.uart_write_string(message)
    basic.show_string(message)
    modify_parameters()
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.HASH), on_uart_data_received)

dernier_temps = 0
compteur_overflow = 0

def get_running_time_total(): # Prévient l'overflow après environ 24 jours
    global dernier_temps, compteur_overflow
    actuel = input.running_time()
    if actuel < dernier_temps:
        # Overflow détecté
        compteur_overflow += 1
    dernier_temps = actuel
    # Chaque overflow ajoute 2**31 ms (~24 jours)
    return compteur_overflow * (2**31) + actuel

def sht31_init():
    # Commande de mesure haute précision sans étirement d'horloge : 0x2C 0x06
    buf = bytearray(2)
    buf[0] = 0x2C
    buf[1] = 0x06
    pins.i2c_write_buffer(0x44, buf)

def get_temp():
    sht31_init()
    basic.pause(50)
    data = pins.i2c_read_buffer(0x44, 6)
    raw_temp = (data[0] << 8) | data[1]
    temp_c = -45 + (175 * raw_temp / 65535)
    return temp_c

def get_hum():
    sht31_init()
    basic.pause(50)
    data = pins.i2c_read_buffer(0x44, 6)
    raw_hum = (data[3] << 8) | data[4]
    humidity = 100 * raw_hum / 65535
    return humidity

def get_date():
    ms = get_running_time_total()

    s = ms // 1000
    m = s // 60
    h = m // 60
    d = h // 24

    sec = s % 60
    min_ = m % 60
    hr = h % 24
    day = (first_date[1] + (d % 30)) % 30
    month = (first_date[0] + (d // 30)) % 12

    new_date = [month if month != 0 else 12,
        day if day != 0 else 1,
        hr,
        min_,
        sec
    ]

    if new_date[0] != first_date[0]:
        saison = saisons[new_date[0] - 1]

    return new_date

def envoyer_message(donnees, mode = 0): # Envoyer signal avec le réseau LoRaWAN
    """
    Parameters
    ----------
    donnee:str
        Donnee à envoyer
    mode:int
        0 -> Envoi de données normales
        1 -> Alerte
        2 -> Autre
    """
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

MIN_HUM_hiver = 65
MIN_TEMP_hiver = 35

MIN_HUM_ete = 80
MIN_TEMP_ete = 38

def on_forever():
    date = get_date()
    serial.write_numbers(date) # Affiche la date sur l'ordinateur
    temp = get_temp()
    hum = get_hum() # ----------------------------------Mettre nom du pin
    if saison == "automne" or saison == "hiver":
        if temp <= MIN_TEMP_hiver: # Modifier valeur
            envoyer_message("")
        if hum >= MIN_HUM_hiver:
            envoyer_message("")
    else:
        if temp <= MIN_TEMP_ete: # Modifier valeur
            envoyer_message("")
        if hum >= 80:
            envoyer_message("")

    basic.pause(1000)

basic.forever(on_forever)
