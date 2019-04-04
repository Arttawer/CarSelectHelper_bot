class Car:

    possible_carcass = ("Седан", "Купэ", "Универсал",
                        "Внедорожник", "Хэтчбек",
                        "Кабриолет", "Минивэн")

    def __init__(self, manufacturer, model, carcass, consumption, cost):
        self.cost = int(cost)
        self.consumption = float(consumption)
        self.carcass = carcass
        self.model = model
        self.manufacturer = manufacturer.capitalize()

    def __repr__(self):
        return f'{self.manufacturer} {self.model} ({self.carcass}), consumption: {self.consumption}'

    def __str__(self):
        return self.__repr__()