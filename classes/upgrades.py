class Upgrade:
    def __init__(self, name: str, price: float, effect: float) -> None:
       self.name = name
       self.price = price
       self.effect = effect
       self.bought = False

    def purchase(self) -> tuple[bool, str]:
        self.bought = True
        return (True, "Purchase successful")

class IncomeUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float) -> None:
        super().__init__(name, price, effect)
