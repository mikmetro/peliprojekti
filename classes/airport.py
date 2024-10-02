from .upgrades import *


class AirPort:
    def __init__(self, name: str, country: str, price: int, co2_generation: int, upgrades: tuple[IncomeUpgrade, Co2Upgrade, SecurityUpgrade]) -> None:
        self.name = name
        self.country = country
        self.price = price
        self.co2_generation = co2_generation
        self.upgrades = upgrades
