class AirPort:
    def __init__(self, name: str, price: int, co2_generation: int) -> None:
        self.name = name
        self.price = price
        self.owned = False