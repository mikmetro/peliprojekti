import os
import time
import threading
import cursor
from pynput import keyboard
from classes.player import *
from classes.airport import *
from classes.upgrades import *
from constants import *
cursor.hide()

def clear(): return os.system('cls' if os.name == 'nt' else 'clear')
clear()

print("Tervetuloa peliin!")

# basic mekanismi
player = Player(input("Anna nimesi: ").lower())
print(player.create_player())

def game_runner():
    while 1:
        # Etene 1 tick
        player.tick()

        # Tick delay
        time.sleep(GAME_TICK)

# Tee threadistä Daemon thread, muuten thread jää pyörimään ikuisesti vaikka main thread loppuu
game_thread = threading.Thread(target=game_runner, daemon=True)
game_thread.start()

def auto_save():
    while 1:
        player.save_profile()
        time.sleep(AUTOSAVE_DELAY)

save_thread = threading.Thread(target=auto_save, daemon=True)
save_thread.start()

current_menu = 1
selected_index = 0

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

def on_press(key):
    global current_menu
    global selected_index
    if hasattr(key, 'char'):
        if key.char in ('1', '2'):
            current_menu = int(key.char)
            selected_index = 0
        elif key.char == '3':
            player.save_profile()
            print("Profile saved")
        elif key.char == '4':
            exit(0)
    if key == keyboard.Key.up:
        selected_index = max(0, selected_index - 1)
    elif key == keyboard.Key.down:
        selected_index = min(len(player.airports) - 1, selected_index + 1)

listener = keyboard.Listener(
    on_press=on_press)
listener.start()
listener.join()