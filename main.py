import os
import time
import threading
import keyboard
import cursor
from classes.player import *
from classes.airport import *
from classes.upgrades import *
from constants import *
cursor.hide()

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
for i in range(5):
    player.purchase_airport(AirPort(f"Number {str(i)} Airport", "Finland", 0,0,upgrades))
player.upgrade_airport(airport, 0)

current_menu = 1
selected_index = 0

def game_runner():
    while 1:
        # Etene 1 tick
        player.tick()

        # Tick delay
        time.sleep(GAME_TICK)

# Tee threadistä Daemon thread, muuten thread jää pyörimään ikuisesti vaikka main thread loppuu
game_thread = threading.Thread(target=game_runner, daemon=True)
game_thread.start()

def console_runner():
    global current_menu
    prev_menu = current_menu
    while 1:
        # Näytä menu
        if prev_menu != current_menu:
            print("\x1b[2J\x1b[3J")
        prev_menu = current_menu
        print(f"\n\n\n")
        if current_menu == 1:
            print(f"{TOP}Your name: {player.name}{CLR}\n{CLR}")
            print(f"Current money: {player.money:.2f}${CLR}")
            print(f"CO2 used: {player.co2_used:.0f}kg/{CO2_BUDGET}kg Diff {CO2_BUDGET - player.co2_used} {CLR}")
            print(HELP_MESSAGE)
        elif current_menu == 2:
            print(f"{TOP}Your name: {player.name}{CLR}\n")
            print(f"- Airports -{CLR}")
            for index, i in enumerate(player.airports):
                # Voi olla olemassa parempi tapa tehdä samanpituiset välit
                name_space = player.cache["airport_max_len"] - len(i.name) + 3
                price_space = player.cache["airport_price_len"] - len(str(i.price)) + 2
                if index == selected_index:
                    print(f"\x1b[7m{CLR}", end="")
                print(f"{i.name}{" "*name_space}{i.price}${" "*price_space}{i.co2_generation:.0f}kg{CLR}\x1b[0m")
            print(HELP_MESSAGE)
        time.sleep(0.04) # 25fps

console_thread = threading.Thread(target=console_runner, daemon=True)
console_thread.start()

def onkeypress(event):
    global selected_index
    global current_menu
    if event.scan_code == 80:
        selected_index = min(len(player.airports) - 1, selected_index + 1)
    elif event.scan_code == 72:
        selected_index = max(0, selected_index - 1)
    elif event.scan_code in (2,3):
        current_menu = event.scan_code - 1
        selected_index = 0

keyboard.on_press(onkeypress)

while 1: 
    if keyboard.is_pressed('3'):
        exit(0)
    time.sleep(0.05)