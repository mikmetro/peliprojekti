from player import * 

class Upgrade:
    def __init__(self, name: str, price: float, effect: float) -> None:
       self.name = name
       self.price = price
       self.effect = effect
       self.level = 0

    def purchase(self, player: Player) -> tuple[bool, str]:
        if self.name in player.upgrades:
            return (False, "Upgrade already owned")
        if player.money < self.price:
            return (False, "Insufficient funds")

        player.money -= self.price
        player.upgrades.append(self.name)

        self.level += 1

        return (True, "Purchase successful")

class IncomeUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float) -> None:
        super().__init__(name, price, effect)
