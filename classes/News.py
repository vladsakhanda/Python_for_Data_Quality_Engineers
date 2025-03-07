from datetime import datetime

DATETIME_FORMAT = "%d/%m/%Y %H.%M"


class News:
    def __init__(self, text: str, city: str):
        self.text = text
        self.city = city
        self.date = datetime.now().strftime(DATETIME_FORMAT)

    def __str__(self):
        return f"News: {self.text}, {self.city}, {self.date} "
