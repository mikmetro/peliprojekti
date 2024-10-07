class Upgrade:
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int, level: int=0) -> None:
        self.name = name
        self.price = price
        self.effect = effect
        self.delta_price = delta_price
        self.delta_effect = delta_effect
        self.max_level = max_level
        self.level = level

    def upgrade(self) -> tuple[bool, str]:
        if self.level == self.max_level:
            return (False, "Upgrade already maxed out")

        self.level += 1

        return (True, "Successfully upgraded")

    def get_price(self) -> float:
        return self.price * (self.delta_price ** self.level)

    def display_price(self) -> str:
        return f"{self.get_price():.2f}$"


class IncomeUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int, level: int=0) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level, level)

    # Laskee kuinka paljon rahaa tuottaa. Level 0 tuottaa myös rahaa
    def get_effect(self) -> float:
        return self.effect * (self.delta_effect ** self.level)

    def display_effect(self) -> str:
        return f"{self.get_effect():.2f}$/s"


class Co2Upgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int, level: int=0) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level, level)

    # Laskee kuinka paljon co2 vähennystä tulee.
    def get_effect(self) -> int:
        return self.effect * (self.level ** self.delta_effect)

    def display_effect(self) -> str:
        return f"-{self.get_effect():.0f}kg/s"


class SecurityUpgrade(Upgrade):
    def __init__(self, name: str, price: float, effect: float, delta_price: float, delta_effect: float, max_level: int, level: int=0) -> None:
        super().__init__(name, price, effect, delta_price, delta_effect, max_level, level)

    # Laskee kertoimen turvallisuudelle. Eli jos tapahtumassa on 1% mahdollisuus se lasketaan (tapahtuma_mahdollisuus * security_multiplier) missä security_multiplier < 1
    def get_effect(self) -> float:
        return 1 - self.effect * (self.delta_effect ** (self.level - 1)) if self.level > 0 else 1

    def display_effect(self) -> str:
        return f"{self.get_effect():.0f}%"
