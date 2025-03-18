import csv
import json
import os
import re
from collections import Counter
from datetime import datetime
from json.decoder import JSONDecodeError
import csv
import os
from collections import Counter

from classes.Feeds import *


class FileProcessor:
    _DEFAULT_FILE = 'feeds.txt'
    VALID_TYPES = ('txt', 'csv', 'json',)
    _VALID_FEEDS = (Feeds.News, Feeds.PrivateAd, Feeds.LuckyNumber)

    _DEFAULT_FOLDER = 'default'
    _DEFAULT_DESTINATION_PATH = _DEFAULT_FOLDER + '/feeds.txt'
    _DEFAULT_PATH = _DEFAULT_FOLDER + '/info.'

    def __init__(self, path: str = None, type: str = None):
        if path is not None and type is None:
            '''As type isn't defined, the program will try to identify it automatically.'''
            self.identify_type_of_file(path)
        elif path is None:
            '''As path is None, default path will be used.'''
            if type not in FileProcessor.VALID_TYPES:
                raise TypeError(
                    f"Unsupported file type '{type}'. Supported types are: {', '.join(FileProcessor.VALID_TYPES)}.")
            else:
                self._type = type

        self._path = path if path else f"{self._DEFAULT_PATH}{type}"

        self.ensure_default_files_and_folder_exist()
        self.ensure_file_exists()

    def __str__(self):
        return f"FileProcessor(path='{self._path}', type='{self._type}')"

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
        if not os.path.exists(self._path):
            raise FileNotFoundError(
                f"File '{self._path}' does not exist.")

        if not self._path.endswith('.' + self._type):
            raise TypeError(
                f"File type does not match requirements for type. It is expected: '{self._type}'.")

    # Getter for the 'path' attribute
    @property
    def get_path(self):
        """Get the file path."""
        return self._path

    # Getter for the 'type' attribute
    @property
    def get_type(self):
        """Get the file type."""
        return self._type

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
        elif self._type in ('txt', 'csv'):
            self.append_all_feeds_from_txt_or_csv_file()

    def append_all_feeds_from_txt_or_csv_file(self):
        feeds_from_file = []

        with open(self._path, "r") as file:
            for line in file:
                line = line.strip()
                instance = create_feed_instance(line)
                print(f"instance with type {type(instance)} has been found: {instance}")
                if instance is not None:
                    feeds_from_file.append(instance)

        print(f'Feeds from file: {self._path} were added to {self._DEFAULT_DESTINATION_PATH} file')

        with open(self._DEFAULT_DESTINATION_PATH, 'a') as file:
            for feed in feeds_from_file:
                file.write(str(feed) + "\n")

        print(f'File {self._path} has been removed.')
        os.remove(self._path)

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

        feeds = []

        if isinstance(data, list):
            for item in data:
                feed = self.process_feed_object(item)
                if feed:
                    feeds.append(feed)
        elif isinstance(data, dict):
            feed = self.process_feed_object(data)
            if feed:
                feeds.append(feed)
        else:
            print(f"Error: Unexpected JSON format in {file_path}. Expected an array or object.")

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
