import random


class LuckyNumber:
    def __init__(self, name: str):
        self.name = name
        self.lucky_number = random.randint(0, 100)

    def __str__(self):
        return f"Lucky Number: {self.name}, your lucky number is {self.lucky_number}!"
