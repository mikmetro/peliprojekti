from .upgrades import *


class AirPort:
    def __init__(self, id: int, name: str, country: str, price: float, co2_generation: int, upgrades: tuple[IncomeUpgrade, Co2Upgrade, SecurityUpgrade]) -> None:
        self.id = id
        self.name = name
        self.country = country
        self.price = price
        self.co2_generation = co2_generation
        self.upgrades = upgrades

    def get(self) -> dict[str, str | int | float | list[dict[str, int | float | str]]]:
        return {
                "id": self.id,
                "country": self.country,
                "price": self.price,
                "co2_generation": self.co2_generation,
                "upgrades": [
                    i.__dict__ for i in self.upgrades
                ]
            }
        
