from microbit import *

# Constantes
END = "\r\n"

def send_command(cmd):
    # Vider le buffer de réception avant d'envoyer
    while uart.any():
        uart.read()
    
    # Envoyer la commande
    full_cmd = cmd + END
    uart.write(full_cmd)
    display.show("S")  # Indicateur d'envoi
    
    # Attendre et lire la réponse
    response = check_response()
    return response

def check_response():
    response_bytes = b''
    timeout_count = 0
    max_timeout = 50  # 5 secondes (50 * 100ms)
    
    while timeout_count < max_timeout:
        if uart.any():
            # Lire les données disponibles
            new_data = uart.read()
            if new_data:
                response_bytes += new_data
                timeout_count = 0  # Reset timeout si on reçoit des données
                
                # Vérifier si on a une réponse complète (se termine par \r\n)
                if b'\r\n' in response_bytes:
                    break
        else:
            sleep(100)  # 100ms
            timeout_count += 1
    
    # Convertir en string et nettoyer
    if response_bytes:
        try:
            response_string = response_bytes.decode('utf-8').strip()
            return response_string
        except:
            # Si le décodage échoue, retourner les bytes bruts
            return str(response_bytes)
    else:
        return None

def init():
    # Configuration UART pour LoRaWAN - syntaxe micro:bit v1
    uart.init(9600, tx=pin14, rx=pin0)
    
    # Attendre un peu pour que l'UART se stabilise
    sleep(1000)
    
    display.show("I")  # Indicateur d'initialisation
    
    # Test de communication
    response = send_command("AT")
    
    # Réinitialiser l'UART pour l'affichage série
    sleep(500)
    uart.init(115200)
    
    if response:
        uart.write("Reponse: " + str(response) + "\n")
        display.show("O")  # OK
    else:
        uart.write("Aucune reponse recue\n")
        display.show("E")  # Erreur

# Test avec plusieurs commandes
def test_lorawan():
    uart.init(9600, tx=pin14, rx=pin0)
    sleep(1000)
    
    commands = ["AT", "AT+VER", "AT+ID"]
    
    for i in range(len(commands)):
        cmd = commands[i]
        display.show(str(i))
        response = send_command(cmd)
        
        # Affichage sur série
        uart.init(115200)
        if response:
            uart.write(cmd + " -> " + str(response) + "\n")
        else:
            uart.write(cmd + " -> Pas de reponse\n")
        
        # Retour en mode LoRaWAN
        uart.init(9600, tx=pin14, rx=pin0)
        sleep(500)

# Lancement
init()

# Décommenter pour tester plusieurs commandes
# test_lorawan()
