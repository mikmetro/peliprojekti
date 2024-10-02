import os
import time
import threading
from classes.player import *
from classes.airport import *
from classes.upgrades import *


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

player.purchase_airport(airport)
player.upgrade_airport(airport, 0)


def game_runner():
    while 1:
        player.tick()
        time.sleep(GAME_TICK)


# Tee threadistä Daemon thread, muuten thread jää pyörimään ikuisesti vaikka main thread loppuu
game_thread = threading.Thread(target=game_runner, daemon=True)
game_thread.start()


while 1:
    print(f"Current money: {player.money:.2f}")
    print(f"CO2 used: {player.co2_used:.2f}")
    time.sleep(GAME_TICK)
    clear()
