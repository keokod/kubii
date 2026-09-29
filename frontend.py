#!/usr/bin/env python3

import tkinter as tk
import RPi.GPIO as GPIO
import random
import urllib.request
import urllib.error


# ============================================================
# CONFIGURATION
# ============================================================

# Taille des cases
CELL_SIZE = 20

GRAY   = "#808080"       # GPIO sans événement
BLUE   = "#0080ff"       # Front montant 0 -> 1
BLACK  = "#000000"       # GND
ORANGE = "#ff8800"       # Entrée aléatoire
RED    = "#ff0000"       # 5 V
YELLOW = "#ffff00"       # 3.3 V

# Anti-rebond en millisecondes
BOUNCE_TIME = 20

# Adresse du Pico
NEXT_URL = "http://192.168.68.90/led"

# Intervalle AUTO
AUTO_INTERVAL = 500       # 500 ms = 0,5 seconde

# Etat du mode automatique
auto_mode = False


# ============================================================
# BROCHAGE PHYSIQUE RASPBERRY PI 4
#
# Numéro physique / Nom / GPIO BCM
# ============================================================

PINS = [

    (1,  "3.3V",   None),
    (2,  "5V",     None),

    (3,  "GPIO2",   2),
    (4,  "5V",     None),

    (5,  "GPIO3",   3),
    (6,  "GND",    None),

    (7,  "GPIO4",   4),
    (8,  "GPIO14", 14),

    (9,  "GND",    None),
    (10, "GPIO15", 15),

    (11, "GPIO17", 17),
    (12, "GPIO18", 18),

    (13, "GPIO27", 27),
    (14, "GND",    None),

    (15, "GPIO22", 22),
    (16, "GPIO23", 23),

    (17, "3.3V",   None),
    (18, "GPIO24", 24),

    (19, "GPIO10", 10),
    (20, "GND",    None),

    (21, "GPIO9",   9),
    (22, "GPIO25", 25),

    (23, "GPIO11", 11),
    (24, "GPIO8",   8),

    (25, "GND",    None),
    (26, "GPIO7",   7),

    (27, "GPIO0",   0),
    (28, "GPIO1",   1),

    (29, "GPIO5",   5),
    (30, "GND",    None),

    (31, "GPIO6",   6),
    (32, "GPIO12", 12),

    (33, "GPIO13", 13),
    (34, "GND",    None),

    (35, "GPIO19", 19),
    (36, "GPIO16", 16),

    (37, "GPIO26", 26),
    (38, "GPIO20", 20),

    (39, "GND",    None),
    (40, "GPIO21", 21),
]


# ============================================================
# LISTE DES GPIO
# ============================================================

GPIO_PINS = [
    gpio
    for physical, name, gpio in PINS
    if gpio is not None
]


# ============================================================
# GPIO AVEC PULL-DOWN
#
# GPIO23 = broche physique 16
# GPIO24 = broche physique 18
#
# Les interrupteurs sont reliés entre 3.3V et GPIO.
#
# Interrupteur ouvert  -> GPIO = LOW
# Interrupteur fermé  -> GPIO = HIGH
# ============================================================

PULL_DOWN_PINS = [23, 24]


# ============================================================
# COMPTEURS DE FRONTS
#
# Seuls les GPIO possèdent un compteur.
#
# GND / 5V / 3.3V :
#   aucun compteur
# ============================================================

front_counts = {
    gpio: 0
    for gpio in GPIO_PINS
}


# ============================================================
# INITIALISATION GPIO
# ============================================================

GPIO.setmode(GPIO.BCM)

for gpio in GPIO_PINS:

    if gpio in PULL_DOWN_PINS:

        GPIO.setup(
            gpio,
            GPIO.IN,
            pull_up_down=GPIO.PUD_DOWN
        )

    else:

        GPIO.setup(
            gpio,
            GPIO.IN
        )


# ============================================================
# INTERFACE TKINTER
# ============================================================

root = tk.Tk()

root.title(
    "Raspberry Pi 4 - GPIO Monitor"
)

root.configure(
    bg="#202020"
)


# ============================================================
# TITRE
# ============================================================

title = tk.Label(
    root,
    text="RASPBERRY PI 4 - GPIO",
    fg="white",
    bg="#202020",
    font=("Arial", 14, "bold")
)

title.pack(
    pady=10
)


# ============================================================
# CONNECTEUR 40 BROCHES
# ============================================================

connector = tk.Frame(
    root,
    bg="#202020"
)

connector.pack(
    padx=20,
    pady=10
)


# ============================================================
# MEMOIRE DES CASES
# ============================================================

boxes = {}


# ============================================================
# COULEUR INITIALE
# ============================================================

def initial_color(name):

    if name == "5V":
        return RED

    if name == "3.3V":
        return YELLOW

    if name == "GND":
        return BLACK

    return GRAY


# ============================================================
# CREATION D'UN ESPACE COMPTEUR
#
# Pour garder parfaitement l'alignement :
#
# GPIO :
#     affiche le compteur
#
# GND / 5V / 3.3V :
#     affiche un espace vide
#
# Les deux ont exactement la même largeur.
# ============================================================

def create_count_area(parent, gpio):

    if gpio is not None:

        count_label = tk.Label(
            parent,
            text="0",
            width=4,
            fg="#ffffff",
            bg="#202020",
            font=("Arial", 8, "bold"),
            anchor="center"
        )

    else:

        # ----------------------------------------------------
        # ESPACE VIDE
        #
        # Même largeur que le compteur.
        # ----------------------------------------------------

        count_label = tk.Label(
            parent,
            text="",
            width=4,
            fg="#202020",
            bg="#202020",
            font=("Arial", 8, "bold"),
            anchor="center"
        )

    count_label.pack(
        side="left",
        padx=3
    )

    return count_label


# ============================================================
# CREATION DES 40 BROCHES
# ============================================================

for row in range(20):

    # ========================================================
    # BROCHE GAUCHE
    # ========================================================

    physical, name, gpio = PINS[row * 2]

    frame_left = tk.Frame(
        connector,
        bg="#202020"
    )

    frame_left.grid(
        row=row,
        column=0,
        padx=5,
        pady=2
    )

    # --------------------------------------------------------
    # NUMERO PHYSIQUE
    # --------------------------------------------------------

    label_left = tk.Label(
        frame_left,
        text=f"{physical:02d}",
        width=3,
        fg="white",
        bg="#202020",
        font=("Arial", 8)
    )

    label_left.pack(
        side="left"
    )

    # --------------------------------------------------------
    # CASE
    # --------------------------------------------------------

    canvas_left = tk.Canvas(
        frame_left,
        width=CELL_SIZE,
        height=CELL_SIZE,
        bg="#202020",
        highlightthickness=0
    )

    canvas_left.pack(
        side="left"
    )

    rectangle_left = canvas_left.create_rectangle(
        0,
        0,
        CELL_SIZE,
        CELL_SIZE,
        fill=initial_color(name),
        outline="white"
    )

    # --------------------------------------------------------
    # COMPTEUR OU ESPACE VIDE
    # --------------------------------------------------------

    count_label_left = create_count_area(
        frame_left,
        gpio
    )

    # --------------------------------------------------------
    # MEMOIRE
    # --------------------------------------------------------

    boxes[physical] = {
        "canvas": canvas_left,
        "rectangle": rectangle_left,
        "gpio": gpio,
        "name": name,
        "count_label": count_label_left
    }


    # ========================================================
    # CENTRE
    # ========================================================

    center = tk.Label(
        connector,
        text="│",
        fg="#606060",
        bg="#202020"
    )

    center.grid(
        row=row,
        column=1
    )


    # ========================================================
    # BROCHE DROITE
    # ========================================================

    physical, name, gpio = PINS[row * 2 + 1]

    frame_right = tk.Frame(
        connector,
        bg="#202020"
    )

    frame_right.grid(
        row=row,
        column=2,
        padx=5,
        pady=2
    )

    # --------------------------------------------------------
    # CASE
    # --------------------------------------------------------

    canvas_right = tk.Canvas(
        frame_right,
        width=CELL_SIZE,
        height=CELL_SIZE,
        bg="#202020",
        highlightthickness=0
    )

    canvas_right.pack(
        side="left"
    )

    rectangle_right = canvas_right.create_rectangle(
        0,
        0,
        CELL_SIZE,
        CELL_SIZE,
        fill=initial_color(name),
        outline="white"
    )

    # --------------------------------------------------------
    # COMPTEUR OU ESPACE VIDE
    # --------------------------------------------------------

    count_label_right = create_count_area(
        frame_right,
        gpio
    )

    # --------------------------------------------------------
    # NUMERO PHYSIQUE
    # --------------------------------------------------------

    label_right = tk.Label(
        frame_right,
        text=f"{physical:02d}",
        width=3,
        fg="white",
        bg="#202020",
        font=("Arial", 8)
    )

    label_right.pack(
        side="left"
    )

    # --------------------------------------------------------
    # MEMOIRE
    # --------------------------------------------------------

    boxes[physical] = {
        "canvas": canvas_right,
        "rectangle": rectangle_right,
        "gpio": gpio,
        "name": name,
        "count_label": count_label_right
    }


# ============================================================
# CHANGER LA COULEUR D'UNE BROCHE
# ============================================================

def set_color(physical, color):

    box = boxes.get(physical)

    if box is None:
        return

    box["canvas"].itemconfig(
        box["rectangle"],
        fill=color
    )


# ============================================================
# METTRE A JOUR LE COMPTEUR
# ============================================================

def update_count_display(physical):

    box = boxes.get(physical)

    if box is None:
        return

    gpio = box["gpio"]

    # --------------------------------------------------------
    # GND / 5V / 3.3V
    #
    # Pas de compteur.
    # --------------------------------------------------------

    if gpio is None:
        return

    count = front_counts.get(
        gpio,
        0
    )

    box["count_label"].config(
        text=str(count),
        fg="#ffffff"
    )


# ============================================================
# INCREMENTER LE COMPTEUR
# ============================================================

def increment_front_count(gpio):

    physical = physical_from_gpio(gpio)

    if physical is None:
        return

    front_counts[gpio] += 1

    update_count_display(
        physical
    )


# ============================================================
# TROUVER LE NUMERO PHYSIQUE
# ============================================================

def physical_from_gpio(gpio):

    for physical, name, gpio_number in PINS:

        if gpio_number == gpio:
            return physical

    return None


# ============================================================
# CALLBACK GPIO
#
# FRONT MONTANT :
#     compteur +1
#     case bleue
#
# FRONT DESCENDANT :
#     compteur +1
#     case reste bleue
# ============================================================

def edge_callback(gpio):

    physical = physical_from_gpio(gpio)

    if physical is None:
        return

    state = GPIO.input(gpio)

    # --------------------------------------------------------
    # COMPTEUR
    # --------------------------------------------------------

    front_counts[gpio] += 1

    root.after(
        0,
        lambda p=physical: update_count_display(p)
    )


    # ========================================================
    # FRONT MONTANT
    # ========================================================

    if state == GPIO.HIGH:

        print(
            f"FRONT MONTANT : "
            f"GPIO{gpio} "
            f"(broche physique {physical}) "
            f"TOTAL = {front_counts[gpio]}"
        )

        root.after(
            0,
            lambda p=physical: set_color(
                p,
                BLUE
            )
        )


    # ========================================================
    # FRONT DESCENDANT
    # ========================================================

    else:

        print(
            f"FRONT DESCENDANT : "
            f"GPIO{gpio} "
            f"(broche physique {physical}) "
            f"TOTAL = {front_counts[gpio]}"
        )

        # La case reste bleue.


# ============================================================
# INSTALLATION DE L'ECOUTE SUR TOUS LES GPIO
# ============================================================

print()
print("Installation de la surveillance GPIO...")
print()

for gpio in GPIO_PINS:

    try:

        GPIO.add_event_detect(
            gpio,
            GPIO.BOTH,
            callback=edge_callback,
            bouncetime=BOUNCE_TIME
        )

        print(
            f"GPIO{gpio:02d} : OK"
        )

    except RuntimeError as error:

        print(
            f"GPIO{gpio:02d} : ERREUR : {error}"
        )


# ============================================================
# ENTREE ALEATOIRE
#
# Appuyer sur R
# ============================================================

random_physical = None


def random_input():

    global random_physical

    gpio_list = [
        physical
        for physical, name, gpio in PINS
        if gpio is not None
    ]

    if not gpio_list:
        return

    # --------------------------------------------------------
    # Ancienne entrée aléatoire -> gris
    # --------------------------------------------------------

    if random_physical is not None:

        set_color(
            random_physical,
            GRAY
        )

    # --------------------------------------------------------
    # Nouvelle entrée
    # --------------------------------------------------------

    random_physical = random.choice(
        gpio_list
    )

    set_color(
        random_physical,
        ORANGE
    )

    print(
        f"ENTREE ALEATOIRE : "
        f"broche physique {random_physical}"
    )


root.bind(
    "r",
    lambda event: random_input()
)

root.bind(
    "R",
    lambda event: random_input()
)


# ============================================================
# REQUETE HTTP - BOUTON SUIVANT
# ============================================================

def suivant():

    print()
    print(
        f"REQUETE HTTP GET : {NEXT_URL}"
    )

    try:

        request = urllib.request.Request(
            NEXT_URL,
            method="GET"
        )

        with urllib.request.urlopen(
            request,
            timeout=3
        ) as response:

            status_code = response.getcode()

            print(
                f"REPONSE HTTP : {status_code}"
            )

            response_data = response.read()

            if response_data:

                print(
                    f"REPONSE : "
                    f"{response_data.decode('utf-8', errors='replace')}"
                )

            status_label.config(
                text=f"HTTP OK : {status_code}",
                fg="#00ff00"
            )


    except urllib.error.HTTPError as error:

        print(
            f"ERREUR HTTP : "
            f"{error.code} - {error.reason}"
        )

        status_label.config(
            text=f"ERREUR HTTP : {error.code}",
            fg="#ff0000"
        )


    except urllib.error.URLError as error:

        print(
            f"ERREUR RESEAU : "
            f"{error.reason}"
        )

        status_label.config(
            text="ERREUR RESEAU",
            fg="#ff0000"
        )


    except Exception as error:

        print(
            f"ERREUR : {error}"
        )

        status_label.config(
            text="ERREUR",
            fg="#ff0000"
        )


# ============================================================
# MODE AUTO
# ============================================================

def auto_suivant():

    global auto_mode

    if not auto_mode:
        return

    suivant()

    root.after(
        AUTO_INTERVAL,
        auto_suivant
    )


def toggle_auto():

    global auto_mode

    # --------------------------------------------------------
    # ARRET AUTO
    # --------------------------------------------------------

    if auto_mode:

        auto_mode = False

        auto_button.config(
            text="AUTO",
            bg="#008000",
            activebackground="#00aa00"
        )

        status_label.config(
            text="Mode AUTO arrêté",
            fg="#aaaaaa"
        )

        print()
        print("MODE AUTO : ARRET")
        print()


    # --------------------------------------------------------
    # DEMARRAGE AUTO
    # --------------------------------------------------------

    else:

        auto_mode = True

        auto_button.config(
            text="STOP AUTO",
            bg="#cc0000",
            activebackground="#ff0000"
        )

        status_label.config(
            text="Mode AUTO : toutes les 0,5 s",
            fg="#00ff00"
        )

        print()
        print("MODE AUTO : DEMARRAGE")
        print("Intervalle : 500 ms")
        print()

        root.after(
            0,
            auto_suivant
        )


# ============================================================
# RESET DU TEST
#
# - Arrête AUTO
# - Remet les GPIO en gris
# - Remet les compteurs GPIO à 0
# - GND reste noir
# - 5V reste rouge
# - 3.3V reste jaune
# ============================================================

def reset_test():

    global auto_mode
    global random_physical

    print()
    print("==============================")
    print(" RESET DU TEST")
    print("==============================")

    # --------------------------------------------------------
    # ARRET AUTO
    # --------------------------------------------------------

    auto_mode = False

    auto_button.config(
        text="AUTO",
        bg="#008000",
        activebackground="#00aa00"
    )


    # --------------------------------------------------------
    # RESET ENTREE ALEATOIRE
    # --------------------------------------------------------

    random_physical = None


    # --------------------------------------------------------
    # RESET DES COMPTEURS
    # --------------------------------------------------------

    for gpio in GPIO_PINS:

        front_counts[gpio] = 0


    # --------------------------------------------------------
    # RESET DES AFFICHAGES
    # --------------------------------------------------------

    for physical, name, gpio in PINS:

        color = initial_color(
            name
        )

        set_color(
            physical,
            color
        )

        # Seulement les GPIO ont un compteur
        if gpio is not None:

            update_count_display(
                physical
            )


    # --------------------------------------------------------
    # STATUT
    # --------------------------------------------------------

    status_label.config(
        text="Test réinitialisé - compteurs à 0",
        fg="#ffff00"
    )

    print(
        "Tous les compteurs GPIO ont été remis à 0."
    )

    print(
        "Toutes les cases ont été réinitialisées."
    )

    print(
        "Mode AUTO arrêté."
    )

    print(
        "Prêt pour un nouveau test."
    )

    print()


# ============================================================
# BOUTONS
# ============================================================

buttons_frame = tk.Frame(
    root,
    bg="#202020"
)

buttons_frame.pack(
    pady=10
)


# ============================================================
# BOUTON SUIVANT
# ============================================================

next_button = tk.Button(
    buttons_frame,
    text="SUIVANT",
    command=suivant,
    width=12,
    height=2,
    bg="#0080ff",
    fg="white",
    activebackground="#00a0ff",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief="raised",
    bd=3,
    cursor="hand2"
)

next_button.pack(
    side="left",
    padx=4
)


# ============================================================
# BOUTON AUTO
# ============================================================

auto_button = tk.Button(
    buttons_frame,
    text="AUTO",
    command=toggle_auto,
    width=12,
    height=2,
    bg="#008000",
    fg="white",
    activebackground="#00aa00",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief="raised",
    bd=3,
    cursor="hand2"
)

auto_button.pack(
    side="left",
    padx=4
)


# ============================================================
# BOUTON RESET
# ============================================================

reset_button = tk.Button(
    buttons_frame,
    text="RESET",
    command=reset_test,
    width=12,
    height=2,
    bg="#ff8800",
    fg="white",
    activebackground="#ffaa00",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief="raised",
    bd=3,
    cursor="hand2"
)

reset_button.pack(
    side="left",
    padx=4
)


# ============================================================
# STATUT
# ============================================================

status_label = tk.Label(
    root,
    text="Prêt",
    fg="#aaaaaa",
    bg="#202020",
    font=("Arial", 9)
)

status_label.pack(
    pady=3
)


# ============================================================
# LEGENDE
# ============================================================

legend = tk.Frame(
    root,
    bg="#202020"
)

legend.pack(
    pady=10
)


def add_legend(color, text):

    frame = tk.Frame(
        legend,
        bg="#202020"
    )

    frame.pack(
        side="left",
        padx=7
    )

    canvas = tk.Canvas(
        frame,
        width=CELL_SIZE,
        height=CELL_SIZE,
        bg="#202020",
        highlightthickness=0
    )

    canvas.pack(
        side="left"
    )

    canvas.create_rectangle(
        0,
        0,
        CELL_SIZE,
        CELL_SIZE,
        fill=color,
        outline="white"
    )

    label = tk.Label(
        frame,
        text=text,
        fg="white",
        bg="#202020",
        font=("Arial", 8)
    )

    label.pack(
        side="left",
        padx=3
    )


add_legend(GRAY, "GPIO")
add_legend(BLUE, "FRONT MONTANT")
add_legend(BLACK, "GND")
add_legend(ORANGE, "ALEATOIRE")
add_legend(RED, "5V")
add_legend(YELLOW, "3.3V")


# ============================================================
# ARRET PROPRE
# ============================================================

def close_program():

    global auto_mode

    print()
    print("Arrêt du programme...")

    # Arrêter AUTO
    auto_mode = False

    # Retirer les événements GPIO
    for gpio in GPIO_PINS:

        try:

            GPIO.remove_event_detect(
                gpio
            )

        except RuntimeError:
            pass

    # Nettoyage GPIO
    GPIO.cleanup()

    # Fermer Tkinter
    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_program
)


# ============================================================
# DEMARRAGE
# ============================================================

print()
print("==============================")
print(" GPIO MONITOR RASPBERRY PI 4")
print("==============================")
print()

print("BLEU   = front montant 0 -> 1")
print("BLEU   = reste bleu après front descendant")
print("COMPTEUR = nombre total de fronts GPIO")

print("GRIS   = GPIO")
print("ORANGE = entrée aléatoire")
print("NOIR   = GND")
print("ROUGE  = 5V")
print("JAUNE  = 3.3V")

print()
print("GND / 5V / 3.3V = aucun compteur")
print()

print("GPIO23 = PULL-DOWN INTERNE")
print("GPIO24 = PULL-DOWN INTERNE")

print()
print("GPIO23 : interrupteur vers 3.3V")
print("GPIO24 : interrupteur vers 3.3V")

print()
print("Touche R : entrée aléatoire")

print()
print(f"Bouton SUIVANT : GET {NEXT_URL}")
print("Bouton AUTO    : toutes les 0,5 secondes")
print("Bouton RESET   : remet cases + compteurs à zéro")

print()
print("Taille des cases : 20 x 20 pixels")
print("Espace compteur réservé pour toutes les broches")
print()
print("Surveillance permanente...")
print()


# ============================================================
# BOUCLE TKINTER
# ============================================================

root.mainloop()
