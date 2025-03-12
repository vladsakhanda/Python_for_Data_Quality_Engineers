import random
import re
from datetime import datetime

DATETIME_FORMAT = "%d/%m/%Y %H.%M"


def is_valid_feed(line):
    return (re.match(Feeds.NEWS_PATTERN, line) or
            re.match(Feeds.LUCKY_NUMBER_PATTERN, line) or
            re.match(Feeds.PRIVATE_AD_PATTERN, line))


def create_feed_instance(line):
    if re.match(Feeds.NEWS_PATTERN, line):
        match = re.match(Feeds.NEWS_PATTERN, line)
        text, city, date = match.groups()
        return Feeds.News(text=text, city=city, date=date)
    elif re.match(Feeds.LUCKY_NUMBER_PATTERN, line):
        match = re.match(Feeds.LUCKY_NUMBER_PATTERN, line)
        name, lucky_number = match.groups()
        return Feeds.LuckyNumber(name=name, lucky_number=lucky_number)
    elif re.match(Feeds.PRIVATE_AD_PATTERN, line):
        match = re.match(Feeds.PRIVATE_AD_PATTERN, line)
        text, expiration_date_str = match.groups()
        expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y")
        return Feeds.PrivateAd(text=text, expiration_date=expiration_date)
    return None


class Feeds:
    DATE_FORMAT = "%d/%m/%Y %H.%M"
    NEWS_PATTERN = r"^News:\s(.+?),\s(.+?),\s(\d{2}/\d{2}/\d{4}\s\d{2}\.\d{2})$"
    LUCKY_NUMBER_PATTERN = r"^Lucky Number:\s(.+?),\syour lucky number is (\d+)!$"
    PRIVATE_AD_PATTERN = r"^Private Ad:\s(.+?),\suntil:\s(\d{2}/\d{2}/\d{4}),\s-?\d+\sdays left$"

    class LuckyNumber:
        def __init__(self, name: str, lucky_number=None):
            self.name = name
            self.lucky_number = lucky_number if lucky_number else random.randint(0, 100)

        def __str__(self):
            return f"Lucky Number: {self.name}, your lucky number is {self.lucky_number}!"

    class News:
        def __init__(self, text: str, city: str, date=None):
            self.text = text
            self.city = city
            self.date = date if date else datetime.now().strftime(DATETIME_FORMAT)

        def __str__(self):
            return f"News: {self.text}, {self.city}, {self.date} "

    class PrivateAd:
        DATETIME_FORMAT = "%d/%m/%Y"

        def __init__(self, text: str, expiration_date: datetime):
            self.text = text
            self.expiration_date = expiration_date

        def __str__(self):
            days_left = (self.expiration_date - datetime.now()).days
            return f"Private Ad: {self.text}, until: {self.expiration_date.strftime(self.DATETIME_FORMAT)}, {days_left} days left"
