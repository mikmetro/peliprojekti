import json
from .airport import *
from .upgrades import *
from .db import *
from constants import GAME_TICK, CO2_BUDGET, SECURITY_BASE, CO2_SAKOT, RANDOM_SAKOT, TIME_LIMIT, WIN_REQUIREMENT
import random

import os.path

db = Database()

class Player:
    def __init__(self, name: str, airports: list[AirPort]) -> None:
        self.name = name
        self.co2_used = 0
        self.money = 0.0
        self.airports: list[AirPort] = []
        self.cache = {
            "airport_max_len": 0,
            "airport_price_len": 0,
            "available_max_len": 0,
            "available_price_max_len": 0
        }
        self.time_left = TIME_LIMIT
        self.game_end = False
        self.available_airports: list[AirPort] = airports

        self.calculate_cache()

    def create_player(self, airports: list[AirPort]):        
        if os.path.isfile(f"profiles/{self.name}.json"):
            try:
                with open(f"profiles/{self.name}.json", "r") as f:
                    user_data = json.load(f)
                    self.name = user_data["name"]
                    self.money = user_data["money"]
                    self.co2_used = user_data["co2_used"]
                    self.time_left = user_data["time_self"]
                    for i in user_data["airports"]:
                        airport = user_data["airports"][i]
                        ups = [airport["upgrades"][j] for j in range(3)]
                        ups = (IncomeUpgrade(*ups[0].values()), Co2Upgrade(*ups[1].values()), SecurityUpgrade(*ups[2].values()))
                        self.airports.append(AirPort(airport['id'], i, airport["country"], airport["price"], airport["co2_generation"], ups))
                    self.cache = user_data["cache"]
                    PLAYER_AIRPORTS = [
                        airport.name for airport in self.airports]
                    AVAILABLE_AIRPORTS: list[AirPort] = [
                        i for i in airports if i.name not in PLAYER_AIRPORTS]
                    self.available_airports = AVAILABLE_AIRPORTS
                    self.calculate_cache()
            except:
                return "Failed to load profile"
        else:
            try:
                db.add_player(self.name, self.money, self.co2_used, self.time_left)
            except:
                return "Failed to create profile"

    # Etene 1 peli tick
    def tick(self) -> None:
        if self.game_end: return
        for i in self.airports:
            self.money += i.upgrades[0].get_effect() * GAME_TICK
            self.co2_used = max(
                0, self.co2_used + (i.co2_generation - i.upgrades[1].get_effect()) * GAME_TICK)

            if self.co2_used > CO2_BUDGET:
                self.money = max(0, self.money - CO2_SAKOT[random.randint(0, len(CO2_SAKOT) - 1)])
                self.co2_used = 0
                print("\x1b[2J\x1b[3J")
                print("Sait sakon ilmasto rikkeestä.")

            if random.random() < (SECURITY_BASE * i.upgrades[2].get_effect()) * GAME_TICK:         # if Random value < (Base + (-Base) * (security/100)) / 100
                print("\x1b[2J\x1b[3J")
                vakavuus = random.randint(1,100)
                if vakavuus <= 10 and len(self.airports) > 1:
                    self.airports.pop(-1)
                    print("Menetit lentokentän vakavasta turvallisuus rikkeestä.")
                else:
                    self.money = max(0, self.money - RANDOM_SAKOT[random.randint(0, len(RANDOM_SAKOT) - 1)])
                    print("Sait sakon turvallisuus rikkeestä.")
        self.time_left = max(0, self.time_left - GAME_TICK)
        if self.time_left == 0 or self.money > WIN_REQUIREMENT:
            self.game_end = True

    # Tämän funktion voi laittaa joskus purchase_airport funktioon
    def give_airport(self, airport: AirPort) -> tuple[bool, str]:
        if airport.name in self.airports:
            return (False, "Airport already owned")

        self.airports.append(airport)
        self.cache["airport_max_len"] = max(
            len(airport.name), self.cache["airport_max_len"])
        self.cache["airport_price_len"] = max(
            len(str(airport.price)), self.cache["airport_price_len"])

        self.calculate_cache()

        self.remove_from_available(airport)
        return (True, "Airport given")

    def purchase_airport(self, airport: AirPort) -> tuple[bool, str]:
        if airport.name in self.airports:
            return (False, "Airport already owned")
        if self.money < airport.price:
            return (False, "Insufficient funds")

        self.money -= airport.price
        self.airports.append(airport)
        self.cache["airport_max_len"] = max(
            len(airport.name), self.cache["airport_max_len"])
        self.cache["airport_price_len"] = max(
            len(str(airport.price)), self.cache["airport_price_len"])

        self.calculate_cache()

        self.remove_from_available(airport)
        return (True, "Purchase successful")

    def remove_from_available(self, airport: AirPort) -> None:
        self.available_airports.pop(self.available_airports.index(airport))
    
    def calculate_cache(self) -> None:
        new_cache = [0, 0]
        for i in self.available_airports:
            new_cache[0] = max(new_cache[0], len(i.name))
            new_cache[1] = max(new_cache[1], len(f"{i.price:.2f}"))
        self.cache["available_max_len"], self.cache["available_price_max_len"] = new_cache

    # Path voi myöhemmin vaihtaa Upgrade luokka tyypiksi
    def upgrade_airport(self, airport: AirPort, path: int) -> tuple[bool, str]:
        upgrade = airport.upgrades[path]
        upgrade_price = upgrade.get_price()
        if self.money < upgrade_price:
            return (False, "Insufficient funds")
        try_upgrade = upgrade.upgrade()
        if try_upgrade[0] == False:
            return try_upgrade

        self.money -= upgrade_price

        return (True, "Purchase successful")

    def save_profile(self) -> None:
        db.update_player(self.name, self.money, self.co2_used, self.time_left)
        with open(f"profiles/{self.name}.json", "w") as f:
            x = {
                "name": self.name,
                "money": self.money,
                "co2_used": self.co2_used,
                "airports": {
                    i.name: i.get() for i in self.airports
                },
                "cache": self.cache,
                "time_self": self.time_left
            }
            json.dump(x, f)

    def display_time(self) -> str:
        minutes = self.time_left // 60
        seconds = self.time_left - minutes * 60
        return f"{minutes:.0f}:{seconds:02.0f}"
