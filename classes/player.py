from .airport import *
from constants import GAME_TICK

class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.co2_used = 0
        self.money = 0.0
        self.airports: list[AirPort] = []

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
