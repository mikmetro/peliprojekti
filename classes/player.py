import json
from .airport import *
from constants import GAME_TICK

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
        dict = {
            "name": self.name,
            "money": self.money,
            "co2_used": self.co2_used,
        }
        
        with open(f"profiles/{self.name}.json", "w") as f:
            json.dump(dict, f)