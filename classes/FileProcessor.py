import csv
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
from collections import Counter
from json.decoder import JSONDecodeError

from classes.Feeds import *


class FileProcessor:
    _DEFAULT_FILE = 'feeds.txt'
    VALID_TYPES = ('txt', 'json', 'xml')
    _DEFAULT_TYPE = 'txt'
    _VALID_FEEDS = (Feeds.News, Feeds.PrivateAd, Feeds.LuckyNumber)

    _DEFAULT_FOLDER = 'default'
    _DEFAULT_DESTINATION_PATH = _DEFAULT_FOLDER + '/feeds.txt'
    _DEFAULT_PATH = _DEFAULT_FOLDER + '/info.'
    _DB = "feeds.db"

    def __init__(self, path: str = None, type: str = None):
        if path and not type:
            '''As type isn't defined, the program will try to identify it automatically.'''
            self.identify_type_of_file(path)
        elif path is None:
            '''As path is None, default path will be used.'''
            if type is not None:
                if type not in FileProcessor.VALID_TYPES:
                    raise TypeError(
                        f"Unsupported file type '{type}'. Supported types are: {', '.join(FileProcessor.VALID_TYPES)}.")
                else:
                    self._type = type
            else:
                self._type = self._DEFAULT_TYPE

        self._path = path if path else f"{self._DEFAULT_PATH}{self._type}"

        self._conn = sqlite3.connect(self._DB)
        self._cursor = self._conn.cursor()

        self.ensure_default_files_and_folder_exist()
        self.ensure_file_exists()
        self.ensure_database_exists()

    def __str__(self):
        return f"FileProcessor(path='{self._path}', type='{self._type}')"

    @property
    def get_path(self):
        """Get the file path."""
        return self._path

    @property
    def get_type(self):
        """Get the file type."""
        return self._type

    def identify_type_of_file(self, path):
        for type in FileProcessor.VALID_TYPES:
            if path.endswith(type):
                self._type = type
                return f'File type is {type}'

        raise TypeError(
            f"Unsupported file type. Supported types are: {', '.join(FileProcessor.VALID_TYPES)}.")

    def ensure_file_exists(self):
        """
        Validates that the file exists and matches the expected type.
        Raises an error if the file does not exist or the type is invalid.
        """
        files_to_check = [
            "1.csv", "1.txt", "1.json", "1.xml",
            "default/info.txt", "default/info.json", "default/info.xml", "default/info.csv"
        ]

        if not os.path.exists(self._path):
            raise FileNotFoundError(
                f"File '{self._path}' does not exist.")

        print(self._path)
        print(self._type)
        if not self._path.endswith('.' + self._type):
            raise TypeError(
                f"File type does not match requirements for type. It is expected: '{self._type}'.")

        for file_path in files_to_check:
            if not os.path.exists(file_path):
                folder = os.path.dirname(file_path)
                if folder and not os.path.exists(folder):
                    os.makedirs(folder, exist_ok=True)

                with open(file_path, "w") as file:
                    file.close()

    def ensure_default_files_and_folder_exist(self):
        """
           Ensures the default folder exists and that a default file is created
           if it does not already exist.
        """
        # Ensure the default folder exists
        if not os.path.exists(self._DEFAULT_FOLDER):
            os.makedirs(self._DEFAULT_FOLDER, exist_ok=True)

        # Ensure the default file exists
        if not os.path.exists(self._path):
            with open(self._path, 'w') as file:
                file.close()

        if not os.path.exists(self._DEFAULT_DESTINATION_PATH):
            with open(self._DEFAULT_DESTINATION_PATH, 'w') as file:
                file.close()

    def append_one_feed_to_file(self, feed: (Feeds.News, Feeds.PrivateAd, Feeds.LuckyNumber)):
        if not type(feed) in self._VALID_FEEDS:
            raise TypeError(
                f"{type(feed)} type does not match requirements for type. It is expected: '{self.VALID_TYPES}'.")

        with open(self._DEFAULT_DESTINATION_PATH, 'a') as file:
            file.write(str(feed) + "\n")

        self.csv_parsing(self._DEFAULT_DESTINATION_PATH)

    def append_all_feeds_from_file(self):
        if self._type == 'json':
            self.append_feeds_from_json()
        elif self._type in ('txt'):
            self.append_all_feeds_from_txt_or_csv_file()
        elif self._type in ('xml'):
            self.append_feeds_from_xml()

    def append_all_feeds_from_txt_or_csv_file(self):
        feeds_from_file = []
        with open(self._path, "r") as file:
            for line in file:
                line = line.strip().split(",")
                if len(line) < 2:
                    continue
                feed_type, *values = [field.strip() for field in line]

                if feed_type.lower() == "news" and len(values) == 2:
                    feeds_from_file.append(Feeds.News(text=values[0], city=values[1]))
                elif feed_type.lower() == "lucky number" and len(values) == 1:
                    feeds_from_file.append(Feeds.LuckyNumber(name=values[0]))
                elif feed_type.lower() == "private add" and len(values) == 2:
                    expiration_date = datetime.strptime(values[1].strip(), "%d/%m/%Y")
                    feeds_from_file.append(Feeds.PrivateAd(text=values[0], expiration_date=expiration_date))

        with open(self._DEFAULT_DESTINATION_PATH, "a") as file:
            for feed in feeds_from_file:
                file.write(str(feed) + "\n")

        for feed in feeds_from_file:
            self.save_one_feed_to_db(feed)

        print(f"Feeds from file: {self._path} were added to {self._DEFAULT_DESTINATION_PATH} file")

        os.remove(self._path)
        print(f"File {self._path} has been removed.")
        self.csv_parsing(self._DEFAULT_DESTINATION_PATH)

    def csv_parsing(self, path: str):
        with open(path, "r") as file:
            text = file.read()

        words = re.findall(r'\b\w+\b', text.lower())
        word_counts = Counter(words)
        with open(self._DEFAULT_FOLDER + "/word_count.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["word", "count"])
            for word, count in word_counts.items():
                writer.writerow([word, count])

        letters = [char for char in text if char.isalpha()]
        letter_counts = Counter(letters)
        uppercase_counts = Counter(c for c in text if c.isupper())
        total_letters = sum(letter_counts.values())
        with open(self._DEFAULT_FOLDER + "/letter_count.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
            for letter, count in sorted(letter_counts.items()):
                uppercase_count = uppercase_counts.get(letter.upper(), 0)
                percentage = (count / total_letters) * 100
                writer.writerow([letter, count, uppercase_count, f"{percentage:.2f}"])

    def ensure_default_folder_exists(self):
        if not os.path.exists(self._DEFAULT_FOLDER):
            os.makedirs(self._DEFAULT_FOLDER, exist_ok=True)

    def append_feeds_from_json(self):
        feeds = self.json_reader(self._path)
        if not feeds:
            print(f"No valid feeds found in {self._path}.")
            return

        with open(self._DEFAULT_DESTINATION_PATH, "a") as destination_file:
            for feed in feeds:
                destination_file.write(str(feed) + "\n")

        print(f"Feeds from '{self._path}' successfully appended to '{self._DEFAULT_DESTINATION_PATH}'.")

        for feed in feeds:
            self.save_one_feed_to_db(feed)

        os.remove(self._path)
        print(f"File '{self._path}' has been removed after successful processing.")

        self.csv_parsing(self._DEFAULT_DESTINATION_PATH)

    def json_reader(self, file_path):
        """
        Reads JSON file and processes either an array of feed objects or a single feed object.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (JSONDecodeError, FileNotFoundError) as e:
            print(f"Error: Could not read or parse file {file_path}. Exception: {e}")
            return None

        if not isinstance(data, list):
            print(f"Error: Expected a list of objects in the JSON file {file_path}.")
            return None

        feeds = []
        for item in data:
            feed_type = item.get('type', '').lower()

            if feed_type == 'news':
                text = item.get('text')
                city = item.get('city')
                if text and city:
                    feeds.append(Feeds.News(text=text, city=city))
                else:
                    print("Error: Missing required fields for News.")

            elif feed_type == 'lucky_number':
                name = item.get('name')
                lucky_number = item.get('lucky_number')
                if name:
                    feeds.append(Feeds.LuckyNumber(name=name, lucky_number=lucky_number))
                else:
                    print("Error: Missing required fields for Lucky Number.")

            elif feed_type == 'private_ad':
                text = item.get('text')
                expiration_date_str = item.get('expiration_date')
                if text and expiration_date_str:
                    try:
                        expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y")
                        feeds.append(Feeds.PrivateAd(text=text, expiration_date=expiration_date))
                    except ValueError:
                        print(
                            f"Error: Invalid date format for Private Ad. Expected 'dd/mm/yyyy', got '{expiration_date_str}'.")
                else:
                    print("Error: Missing required fields for Private Ad.")

            else:
                print(f"Error: Unsupported feed type '{feed_type}' in JSON.")

        return feeds

    def process_feed_object(self, item):
        """
        Processes a single feed object and converts it to a corresponding Feeds instance.
        """
        feed_type = item.get('type')

        if feed_type == 'private_ad':
            text = item.get("text")
            expiration_date_str = item.get("expiration_date")
            if text and expiration_date_str:
                try:
                    expiration_date = datetime.strptime(expiration_date_str, Feeds.PrivateAd.DATETIME_FORMAT)
                    return Feeds.PrivateAd(text, expiration_date)
                except ValueError:
                    print(f"Error: Invalid expiration date `{expiration_date_str}`")
            else:
                print("Error: Missing required fields for Private Ad.")
        elif feed_type == 'news':
            text = item.get("text")
            city = item.get("city")
            date = item.get("date")
            if text and city:
                return Feeds.News(text, city, date)
            else:
                print("Error: Missing required fields for News.")
        elif feed_type == 'lucky_number':
            name = item.get("name")
            lucky_number = item.get("lucky_number")
            if name:
                return Feeds.LuckyNumber(name, lucky_number)
            else:
                print("Error: Missing required fields for Lucky Number.")
        else:
            print(f"Error: Unrecognized feed type `{feed_type}`.")

        return None

    def append_feeds_from_xml(self, file_path=None):
        """
        Processes an XML file containing feed records.
        """
        if not file_path:
            file_path = self._path

        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return None

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            feeds = []
            for feed in root.findall("feed"):
                feed_type = feed.get("type", "").lower()

                if feed_type == "news":
                    text = feed.find("text").text
                    city = feed.find("city").text
                    if text and city:
                        feeds.append(Feeds.News(text=text, city=city))
                    else:
                        print("Error: Missing required fields for News.")

                elif feed_type == "lucky_number":
                    name = feed.find("name").text
                    lucky_number = feed.find("lucky_number").text
                    lucky_number = int(lucky_number) if lucky_number else None
                    if name:
                        feeds.append(Feeds.LuckyNumber(name=name, lucky_number=lucky_number))
                    else:
                        print("Error: Missing required fields for Lucky Number.")

                elif feed_type == "private_ad":
                    text = feed.find("text").text
                    expiration_date_str = feed.find("expiration_date").text
                    if text and expiration_date_str:
                        try:
                            expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y")
                            feeds.append(Feeds.PrivateAd(text=text, expiration_date=expiration_date))
                        except ValueError:
                            print(
                                f"Error: Invalid date format for Private Ad. Expected 'dd/mm/yyyy', got '{expiration_date_str}'.")
                    else:
                        print("Error: Missing required fields for Private Ad.")

                else:
                    print(f"Error: Unsupported feed type '{feed_type}' in XML.")

            with open(self._DEFAULT_DESTINATION_PATH, "a") as destination_file:
                for feed in feeds:
                    destination_file.write(str(feed) + "\n")

            for feed in feeds:
                self.save_one_feed_to_db(feed)

            os.remove(file_path)
            print(f"File {file_path} successfully processed and removed.")

            return feeds

        except ET.ParseError as e:
            print(f"Error: Failed to parse XML file {file_path}. Exception: {e}")
            return None
        except Exception as e:
            print(f"Error: An unexpected error occurred while processing {file_path}. Exception: {e}")
            return None

    def ensure_database_exists(self):
        self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    city TEXT NOT NULL,
                    date TEXT NOT NULL,
                    UNIQUE(text, city, date)
                )
                """)

        self._cursor.execute("""
                    CREATE TABLE IF NOT EXISTS lucky_number (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        lucky_number INTEGER NOT NULL,
                        UNIQUE(name, lucky_number)
                    )
                    """)
        self._cursor.execute("""
                    CREATE TABLE IF NOT EXISTS private_ad (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        expiration_date TEXT NOT NULL,
                        UNIQUE(text, expiration_date)
                    )
                    """)

        self._conn.commit()

    def save_one_feed_to_db(self, feed: (Feeds.News, Feeds.LuckyNumber, Feeds.PrivateAd)):
        if type(feed) is Feeds.LuckyNumber:
            self._save_lucky_number_to_db(feed)
        elif type(feed) is Feeds.News:
            self._save_news_to_db(feed)
        elif type(feed) is Feeds.PrivateAd:
            self._save_private_ad_to_db(feed)

    def _save_lucky_number_to_db(self, lucky_number: Feeds.LuckyNumber):
        try:
            self._cursor.execute("""
                INSERT INTO lucky_number (name, lucky_number)
                VALUES (?, ?)
                """, (lucky_number.name, lucky_number.lucky_number))
            self._conn.commit()
            print("Lucky Number saved to database.")
        except sqlite3.IntegrityError:
            print("Duplicate Lucky Number record. Not saved.")

    def _save_news_to_db(self, news: Feeds.News):
        try:
            self._cursor.execute("""
                INSERT INTO news (text, city, date)
                VALUES (?, ?, ?)
                """, (news.text, news.city, news.date))
            self._conn.commit()
            print("News saved to database.")
        except sqlite3.IntegrityError:
            print("Duplicate News record. Not saved.")

    def _save_private_ad_to_db(self, private_ad: Feeds.PrivateAd):
        try:
            self._cursor.execute("""
            INSERT INTO private_ad (text, expiration_date)
            VALUES (?, ?)
            """, (private_ad.text, private_ad.expiration_date.strftime(private_ad.DATETIME_FORMAT)))
            self._conn.commit()
            print("Private Ad saved to database.")
        except sqlite3.IntegrityError:
            print("Duplicate Private Ad record. Not saved.")
