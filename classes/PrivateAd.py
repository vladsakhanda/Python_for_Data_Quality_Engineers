from datetime import datetime

class PrivateAd:
    DATETIME_FORMAT = "%d/%m/%Y"

    def __init__(self, text: str, expiration_date: datetime):
        self.text = text
        self.expiration_date = expiration_date

    def __str__(self):
        days_left = (self.expiration_date - datetime.now()).days
        return f"Private Ad: {self.text}, until: {self.expiration_date.strftime(self.DATETIME_FORMAT)}, {days_left} days left"
