class Upgrade:
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int) -> None:
        self.name = name
        self.price = price
        self.effect = effect
        self.delta_price = delta_price
        self.delta_effect = delta_effect
        self.max_level = max_level
        self.level = 0


class IncomeUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level)

    # Laskee kuinka paljon rahaa tuottaa. Level 0 tuottaa myös rahaa
    def tick(self) -> float:
        return self.effect * (self.delta_effect ** self.level)


class Co2Upgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level)

    # Laskee kuinka paljon co2 vähennystä tulee.
    def co2_decrease(self) -> int:
        return self.effect * (self.level ** self.delta_effect)


class SecurityUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level)

    # Laskee kertoimen turvallisuudelle. Eli jos tapahtumassa on 1% mahdollisuus se lasketaan (tapahtuma_mahdollisuus * security_multiplier) missä security_multiplier < 1
    def security_multiplier(self) -> int:
        return 1 - self.effect * (self.delta_effect ** (self.level - 1)) if self.level > 0 else 0
