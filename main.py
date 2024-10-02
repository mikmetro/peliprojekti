import os
import time
import threading
import keyboard
from classes.player import *
from classes.airport import *
from classes.upgrades import *
from constants import *


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


clear()


CO2_BUDGET = 100000  # Jos pelaaja päästää enemmän co2 kuin tämä luku häviät pelin

print("Tervetuloa peliin!")

# basic mekanismi
player = Player(input("Anna nimesi: "))
player.money = 100000
upgrades = (
    IncomeUpgrade("Tuotto", 10000, 5000, 1.5, 1.5, 5),
    Co2Upgrade("Co2", 10000, 5000, 1.5, 1.5, 5),
    SecurityUpgrade("Security", 10000, 5000, 1.5, 1.5, 5)
)
airport = AirPort("Los Angeles Airport", "Iceland", 50000, 10, upgrades)
airportt = AirPort("Abu Dhabi Airport", "Iceland", 50000, 10, upgrades)


player.purchase_airport(airport)
player.purchase_airport(airportt)

player.upgrade_airport(airport, 0)

current_menu = 1

def game_runner():
    global current_menu
    prev_menu = current_menu
    while 1:
        player.tick()
        
        if prev_menu != current_menu:
            print(f"\x1b[2J")
        prev_menu = current_menu
        print(f"\n\n\n{TOP}")
        if current_menu == 1:
            print(f"{TOP}Your name: {player.name}{CLR}\n{CLR}")
            print(f"Current money: {player.money:.2f}{CLR}")
            print(f"CO2 used: {player.co2_used}{CLR}")
            print(HELP_MESSAGE)
        if current_menu == 2:
            print(f"{TOP}Your name: {player.name}{CLR}\n")
            print(f"- Airports -{CLR}")
            for i in player.airports:
                print(f"{i.name}{CLR}")
            print(HELP_MESSAGE)
        time.sleep(GAME_TICK)


# Tee threadistä Daemon thread, muuten thread jää pyörimään ikuisesti vaikka main thread loppuu
game_thread = threading.Thread(target=game_runner, daemon=True)
game_thread.start()

while 1:
    if keyboard.is_pressed('1'):
        current_menu = 1

    elif keyboard.is_pressed('2'):
        current_menu = 2

    elif keyboard.is_pressed('3'):
        current_menu = 3
