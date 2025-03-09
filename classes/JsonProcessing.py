import json
from datetime import datetime
from json.decoder import JSONDecodeError
from classes.Feeds import Feeds, DATETIME_FORMAT

DATE_ONLY_FORMAT = "%d/%m/%Y"
DEFAULT_FILE = 'default_news_feed.txt'
DEFAULT_JSON_FILE = 'default_news_feed.json'

def __init__(self, file_path='feeds.json'):
    self.file_path = file_path


def json_reader(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (JSONDecodeError, FileNotFoundError):
        return None

    feeds = []
    for item in data:
        feed_type = item['type']
        if feed_type == 'lucky_number':
            feeds.append(Feeds.LuckyNumber(item['name']))
        elif feed_type == 'news':
            feeds.append(Feeds.News(item['text'], item['city'], None))
        elif feed_type == 'private_ad':
            expiration_date = datetime.strptime(item['expiration_date'], Feeds.PrivateAd.DATETIME_FORMAT)
            feeds.append(Feeds.PrivateAd(item['text'], expiration_date))

    return feeds

def create_default_JSON_file(feeds_file, JSON_feeds_file):
    with open(feeds_file, 'r') as file1:
        lines_list = file1.readlines()

    objects_list = []
    for line in lines_list:
        if line.startswith("Lucky Number:"):
            name = line.split("Lucky Number:")[1].split(",")[0].strip()
            objects_list.append(Feeds.LuckyNumber(name).to_dict())
        elif line.startswith("Private Ad:"):
            parts = line.split(", until:")
            text = parts[0].split(":")[1].strip()
            date_str = parts[1].split(",")[0].strip()
            expiration_date = datetime.strptime(date_str, Feeds.PrivateAd.DATETIME_FORMAT)
            objects_list.append(Feeds.PrivateAd(text, expiration_date).to_dict())
        elif line.startswith("News:"):
            parts = line.split(", ")
            text = parts[0].split(":")[1].strip()
            city = parts[1].strip()
            date_str = parts[2].strip()
            news1 = Feeds.News(text, city, date_str)
            print(str(news1))
            objects_list.append(Feeds.News(text, city, date_str).to_dict())

        with open(JSON_feeds_file, 'w') as file2:
            json.dump(objects_list, file2, indent=4)
