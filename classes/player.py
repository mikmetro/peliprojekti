import json
from .airport import *
from .upgrades import *
from constants import GAME_TICK
import os.path

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.co2_used = 0
        self.money = 0.0
        self.airports: list[AirPort] = []
        self.cache = {
            "airport_max_len": 0,
            "airport_price_len": 0
        }
        
    def create_player(self):
        if os.path.isfile(f"profiles/{self.name}.json"):
            try:
                with open(f"profiles/{self.name}.json", "r") as f:
                    x = json.load(f)
                    self.name = x["name"]
                    self.money = x["money"]
                    self.co2_used = x["co2_used"]
                    for i in x["airports"]:
                        self.airports.append(AirPort(i, x["airports"][i]["country"], x["airports"][i]["price"], x["airports"][i]["co2_generation"], x["airports"][i]["upgrades"]))
            except:
                return f"Failed to load profile"
        else:
            try:
                with open(f"profiles/{self.name}.json", "w") as f:
                    json.dump({
                        "name": self.name,
                        "money": self.money,
                        "co2_used": self.co2_used,
                        "airports": {},
                    }, f)
                    return "Profile created succsessfully"
            except:
                return "Failed to create profile"
          
    # Etene 1 peli tick
    def tick(self) -> None:
        for i in self.airports:
            self.money += i.upgrades[0].tick() * GAME_TICK
            self.co2_used += (i.co2_generation -
                              i.upgrades[1].co2_decrease()) * GAME_TICK

    def purchase_airport(self, airport: AirPort) -> tuple[bool, str]:
        if airport.name in self.airports:
            return (False, "Airport already owned")
        if self.money < airport.price:
            return (False, "Insufficient funds")

        self.money -= airport.price
        self.airports.append(airport)
        self.cache["airport_max_len"] = max(len(airport.name), self.cache["airport_max_len"])
        self.cache["airport_price_len"] = max(len(str(airport.price)), self.cache["airport_price_len"])

        return (True, "Purchase successful")

    def upgrade_airport(self, airport: AirPort, path: int) -> tuple[bool, str]:
        upgrade = airport.upgrades[path]
        if self.money < upgrade.price:
            return (False, "Insufficient funds")
        if upgrade.level == upgrade.max_level:
            return (False, "Upgrade already maxed out")

        self.money -= upgrade.price * (upgrade.delta_price ** upgrade.level)

        upgrade.level += 1

        return (True, "Purchase successful")

    def save_profile(self) -> None:
        with open(f"profiles/{self.name}.json", "w") as f:
            x = {
            "name": self.name,
            "money": self.money,
            "co2_used": self.co2_used,
            "airports": {
                i.name: {
                    "country": i.country,
                    "price": i.price,
                    "co2_generation": i.co2_generation,
                } for i in self.airports
            }
        }
            json.dump(x, f)