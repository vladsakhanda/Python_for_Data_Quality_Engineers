import random
from datetime import datetime

DATETIME_FORMAT = "%d/%m/%Y %H.%M"


class Feeds:

    class LuckyNumber:
        def __init__(self, name: str):
            self.name = name
            self.lucky_number = random.randint(0, 100)

        def __str__(self):
            return f"Lucky Number: {self.name}, your lucky number is {self.lucky_number}!"

        def to_dict(self):
            return {
                "type": "lucky_number",
                "name": self.name,
            }

    class News:
        def __init__(self, text: str, city: str, date):
            self.text = text
            self.city = city
            if date is None:
                self.date = datetime.now().strftime(DATETIME_FORMAT)
            else:
                self.date = date

        def __str__(self):
            return f"News: {self.text}, {self.city}, {self.date} "

        def to_dict(self):
            return {
                "type": "news",
                "text": self.text,
                "city": self.city,
                "date": self.date
            }

    class PrivateAd:
        DATETIME_FORMAT = "%d/%m/%Y"

        def __init__(self, text: str, expiration_date: datetime):
            self.text = text
            self.expiration_date = expiration_date

        def __str__(self):
            days_left = (self.expiration_date - datetime.now()).days
            return f"Private Ad: {self.text}, until: {self.expiration_date.strftime(self.DATETIME_FORMAT)}, {days_left} days left"

        def to_dict(self):
            return {
                "type": "private_ad",
                "text": self.text,
                "expiration_date": self.expiration_date.strftime(self.DATETIME_FORMAT)
            }



