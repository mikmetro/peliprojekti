from sys import path
import os
import random
import time
import threading
from classes.upgrades import *

CO2_BUDGET = 100000 # Jos pelaaja päästää enemmän co2 kuin tämä luku häviät pelin
GAME_TICK = 0.2
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

money = 0

def game_runner():
    global money
    while 1:
        money += 1
        # Game logic above
        time.sleep(GAME_TICK)

game_thread = threading.Thread(target=game_runner)
game_thread.start()

while 1:
    print(f"Current money: {money}")
    time.sleep(0.5)
    clear()