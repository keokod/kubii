from machine import Pin
import network
import socket
import time

# ============================================================
# WIFI
# ============================================================

SSID = "xxx"
PASSWORD = "xxx"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Connexion au WiFi...")
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep_ms(500)
    print(".", end="")

ip = wlan.ifconfig()[0]

print()
print("WiFi connecté")
print("IP :", ip)

# ============================================================
# GPIO
# ============================================================

gpio_list = [
    0, 2, 3, 6, 10, 11, 12, 13,
    14, 15, 17, 19, 22, 26, 27,
    4, 5, 18, 28, 8, 7, 1, 09,
    16,20,21
]

# Configuration des GPIO en sortie
pins = [Pin(gpio, Pin.OUT) for gpio in gpio_list]

# Tous les GPIO à 0 au démarrage
for pin in pins:
    pin.value(0)

# Index du prochain GPIO à utiliser
gpio_index = 0


# ============================================================
# GENERATION DU FRONT
# ============================================================

def generer_front(pin, gpio):
    print("Front sur GPIO", gpio)

    # Front montant
    pin.value(1)

    # Durée du niveau haut
    time.sleep_ms(250)

    # Front descendant
    pin.value(0)

    # Durée du niveau bas
    time.sleep_ms(250)


# ============================================================
# SERVEUR HTTP
# ============================================================

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

serveur = socket.socket()
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(addr)
serveur.listen(1)

print()
print("Serveur HTTP démarré")
print("URL : http://" + ip + "/led")
print()


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

while True:

    client, adresse = serveur.accept()

    try:
        requete = client.recv(1024).decode()

        print("Requête :", requete.split("\r\n")[0])

        # ----------------------------------------------------
        # GET /led
        # ----------------------------------------------------

        if requete.startswith("GET /led"):

            # GPIO actuel
            gpio = gpio_list[gpio_index]
            pin = pins[gpio_index]

            print("GPIO sélectionné :", gpio)

            # Génération du front
            generer_front(pin, gpio)

            # Passage au GPIO suivant
            gpio_index += 1

            # Retour au début après le dernier GPIO
            if gpio_index >= len(gpio_list):
                gpio_index = 0

            print("Prochain GPIO :", gpio_list[gpio_index])

            reponse = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Connection: close\r\n"
                "\r\n"
                '{"status":"ok","gpio":' + str(gpio) + "}"
            )

        # ----------------------------------------------------
        # GET /
        # ----------------------------------------------------

        elif requete.startswith("GET / "):

            reponse = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<html>"
                "<body>"
                "<h1>Pico GPIO</h1>"
                "<p>GPIO actuel : " +
                str(gpio_list[gpio_index]) +
                "</p>"
                "<p><a href='/led'>GPIO suivant</a></p>"
                "</body>"
                "</html>"
            )

        # ----------------------------------------------------
        # AUTRE URL
        # ----------------------------------------------------

        else:

            reponse = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n"
                "\r\n"
                "Not Found"
            )

        client.send(reponse)

    except Exception as e:
        print("Erreur :", e)

    finally:
        client.close()

