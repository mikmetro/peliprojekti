import json
from .airport import *
from .upgrades import *
from constants import GAME_TICK
import os.path

from classes import upgrades

class Player:
    def __init__(self, name: str, airports: list[AirPort]) -> None:
        self.name = name
        self.co2_used = 0
        self.money = 0.0
        self.airports: list[AirPort] = []
        self.cache = {
            "airport_max_len": 0,
            "airport_price_len": 0
        }
        self.available_airports: list[AirPort] = airports
        
    def create_player(self, airports: list[AirPort]):
        if os.path.isfile(f"profiles/{self.name}.json"):
            try:
                with open(f"profiles/{self.name}.json", "r") as f:
                    user_data = json.load(f)
                    self.name = user_data["name"]
                    self.money = user_data["money"]
                    self.co2_used = user_data["co2_used"]
                    for i in user_data["airports"]:
                        airport = user_data["airports"][i]
                        ups = [airport["upgrades"][j] for j in range(3)]
                        ups = (IncomeUpgrade(*ups[0].values()), Co2Upgrade(*ups[1].values()), SecurityUpgrade(*ups[2].values()))
                        self.airports.append(AirPort(i, airport['id'], airport["country"], airport["price"], airport["co2_generation"], ups))
                    self.cache = user_data["cache"]
                    PLAYER_AIRPORTS = [airport.name for airport in self.airports]
                    AVAILABLE_AIRPORTS: list[AirPort] = [i for i in airports if i.name not in PLAYER_AIRPORTS]
                    self.available_airports = AVAILABLE_AIRPORTS
            except:
                return "Failed to load profile"
        else:
            try:
                self.save_profile()
            except:
                return "Failed to create profile"
          
    # Etene 1 peli tick
    def tick(self) -> None:
        for i in self.airports:
            self.money += i.upgrades[0].tick() * GAME_TICK
            self.co2_used += (i.co2_generation -
                              i.upgrades[1].co2_decrease()) * GAME_TICK

    # Tämän funktion voi laittaa joskus purchase_airport funktioon
    def give_airport(self, airport: AirPort) -> tuple[bool, str]:
        if airport.name in self.airports:
            return (False, "Airport already owned")

        self.airports.append(airport)
        self.cache["airport_max_len"] = max(len(airport.name), self.cache["airport_max_len"])
        self.cache["airport_price_len"] = max(len(str(airport.price)), self.cache["airport_price_len"])

        self.remove_from_available(airport)
        return (True, "Airport given")

    def purchase_airport(self, airport: AirPort) -> tuple[bool, str]:
        if airport.name in self.airports:
            return (False, "Airport already owned")
        if self.money < airport.price:
            return (False, "Insufficient funds")

        self.money -= airport.price
        self.airports.append(airport)
        self.cache["airport_max_len"] = max(len(airport.name), self.cache["airport_max_len"])
        self.cache["airport_price_len"] = max(len(str(airport.price)), self.cache["airport_price_len"])

        self.remove_from_available(airport)
        return (True, "Purchase successful")

    def remove_from_available(self, airport: AirPort) -> None:
        self.available_airports.pop(self.available_airports.index(airport))

    # Path voi myöhemmin vaihtaa Upgrade luokka tyypiksi
    def upgrade_airport(self, airport: AirPort, path: int) -> tuple[bool, str]:
        upgrade = airport.upgrades[path]
        if self.money < upgrade.price:
            return (False, "Insufficient funds")

        upgradestatus = upgrade.upgrade()

        if upgradestatus[0] == False:
            return upgradestatus
            
        self.money -= upgrade.price


        return (True, "Purchase successful")

    def save_profile(self) -> None:
        with open(f"profiles/{self.name}.json", "w") as f:
            x = {
                "name": self.name,
                "money": self.money,
                "co2_used": self.co2_used,
                "airports": {
                    i.name: i.get() for i in self.airports
                },
                "cache": self.cache
            }
            json.dump(x, f)