import os
import time
import threading
import cursor
from pynput import keyboard
from classes.player import *
from classes.airport import *
from classes.upgrades import *
from classes.db import *
from classes.db import *
from constants import *
from random import randint
cursor.hide()

def clear(): return os.system('cls' if os.name == 'nt' else 'clear')
clear()

print("Tervetuloa peliin!")

keyboard_controller = keyboard.Controller()
db = Database()
upgrades = db.upgrades()
airports = db.all_airports()

ALL_AIRPORTS: list[AirPort] = [
    AirPort(i['id'], i['name'], i['municipality'], i['price'], i['co2_generation'], (IncomeUpgrade(**upgrades[0]), Co2Upgrade(**upgrades[1]), SecurityUpgrade(**upgrades[2]))) for i in airports
]

# basic mekanismi
player = Player(input("Anna nimesi: ").lower(), ALL_AIRPORTS)
print(player.create_player(ALL_AIRPORTS))

if len(player.airports) == 0:
    player.give_airport(ALL_AIRPORTS[randint(0, len(ALL_AIRPORTS) - 1)])

def game_runner():
    while 1:
        # Etene 1 tick
        player.tick()

        # Tick delay
        time.sleep(GAME_TICK)

# Tee threadistä Daemon thread, muuten thread jää pyörimään ikuisesti vaikka main thread loppuu
game_thread = threading.Thread(target=game_runner, daemon=True)
game_thread.start()

time_till_save = AUTOSAVE_DELAY
def auto_save():
    global time_till_save
    while 1:
        time.sleep(1)
        time_till_save -= 1
        if(time_till_save == 0):
            player.save_profile()
            time_till_save = AUTOSAVE_DELAY

save_thread = threading.Thread(target=auto_save, daemon=True)
save_thread.start()

current_menu = 1
selected_index = 0
selected_tab = 0
airport_index = 0

def console_runner():
    global current_menu
    global selected_tab
    prev_menu = current_menu
    prev_tab = selected_tab

    HELP_MESSAGE = lambda: f"{CLR}{DOWN}1 - Main{CLR}\n2 - Airports{CLR}\n3 - Save ({time_till_save}){CLR}\n4 - Quit{CLR}"
    
    print("\x1b[2J\x1b[3J")
    while 1:
        # Näytä menu
        if prev_menu != current_menu or prev_tab != selected_tab:
            print("\x1b[2J\x1b[3J")
        prev_menu = current_menu
        prev_tab = selected_tab
        print(f"\n\n\n")
        print(f"{TOP}Your name: {player.name}{CLR}\n")

        if current_menu == 1:
            print(f"Current money: {player.money:.2f}${CLR}")
            print(f"CO2 used: {player.co2_used:.0f}kg/{CO2_BUDGET}kg Diff {(CO2_BUDGET - player.co2_used):.0f} {CLR}")

        elif current_menu == 2:
            for index , i in enumerate(AIRPORT_MENU_TABS):
                if index == selected_tab:
                    print(f"\x1b[7m{CLR}", end="")
                print(i + f"\x1b[0m" + " "*5, end="")
            print("\x1b[0m\n")
            
            if selected_tab == 0:
                print("Press Enter to select")
                for index, i in enumerate(player.airports):
                    # Voi olla olemassa parempi tapa tehdä samanpituiset välit
                    name_space = player.cache["airport_max_len"] - len(i.name) + 3
                    price_space = player.cache["airport_price_len"] - len(str(i.price)) + 2
                    if index == selected_index:
                        print(f"\x1b[7m{CLR}", end="")
                    print(f"{i.name}{" "*name_space}{i.price}${" "*price_space}{i.co2_generation:.0f}kg{CLR}\x1b[0m")
            elif selected_tab == 1:
                print("Press Enter to purchase")
                for index, i in enumerate(player.available_airports):
                    # Voi olla olemassa parempi tapa tehdä samanpituiset välit
                    name_space = player.cache["airport_max_len"] - len(i.name) + 3
                    price_space = player.cache["airport_price_len"] - len(str(i.price)) + 2
                    if index == selected_index:
                        print(f"\x1b[7m{CLR}", end="")

                    # Jos pelaaja pystyy ostamaan lentokentän muuta hinnan väri vihreäksi, muuten väri on punainen
                    price_indicator = (f"\x1b[31m" if i.price > player.money else f"\x1b[32m") + str(i.price) + f"\x1b[39m"

                    print(f"{i.name}{" "*name_space}{price_indicator}${" "*price_space}{i.co2_generation:.0f}kg{CLR}\x1b[0m")

        elif current_menu == 11:
            print(f"{player.airports[airport_index].name}\n")
            ups = player.airports[airport_index].upgrades

            largest_name = [0,0,0]
            for i in ups:
                largest_name[0] = max(largest_name[0], len(i.name))
                largest_name[1] = max(largest_name[1], len(i.display_effect()))
                largest_name[2] = max(largest_name[2], len(i.display_price()))
            
            print("Press Enter to upgrade")
            for (index, i) in enumerate(ups):
                if index == selected_index:
                        print(f"\x1b[7m{CLR}", end="")
                print(f"{i.name} {i.level}{" "*(largest_name[0] - len(i.name) + 3)}{i.display_effect()}{" "*(largest_name[1] - len(i.display_effect()) + 3)}{i.display_price()}\x1b[0m")

        print(HELP_MESSAGE())
        time.sleep(0.04) # 25fps

console_thread = threading.Thread(target=console_runner, daemon=True)
console_thread.start()

def on_press(key):
    global current_menu
    global selected_index
    global time_till_save
    global selected_tab
    global airport_index
    if hasattr(key, 'char'):
        if key.char in ('1', '2'):
            current_menu = int(key.char)
            selected_index = 0
        elif key.char == '3':
            player.save_profile()
            time_till_save = AUTOSAVE_DELAY
            print("Profile saved")
        elif key.char == '4':
            exit(0)
    match key:
        case keyboard.Key.up:
            selected_index = max(0, selected_index - 1)
        case keyboard.Key.down:
            if current_menu == 2:
                if selected_tab == 0:
                    selected_index = min(len(player.airports) - 1, selected_index + 1)
                elif selected_tab == 1:
                    selected_index = min(len(player.available_airports) - 1, selected_index + 1)
            elif current_menu == 11:
                selected_index = min(len(player.airports[airport_index].upgrades) - 1, selected_index + 1)
        case keyboard.Key.left:
            selected_tab = max(0, selected_tab - 1)
            selected_index = 0
        case keyboard.Key.right:
            selected_tab = min(len(AIRPORT_MENU_TABS) - 1, selected_tab + 1)
            selected_index = 0
        case keyboard.Key.enter:
            if current_menu == 2:
                if selected_tab == 0:
                    if len(player.airports) != 0:
                        # Avaa lentokentän info ja päivitykset
                        current_menu = 11
                        airport_index = selected_index
                        selected_index = 0
                elif selected_tab == 1:
                    if len(player.available_airports) != 0 and player.purchase_airport(player.available_airports[selected_index])[0]:
                        clear()
            elif current_menu == 11:
                player.airports[airport_index].upgrades[selected_index].upgrade()
            keyboard_controller.release(keyboard.Key.enter)


listener = keyboard.Listener(
    on_press=on_press)
listener.start()
listener.join()