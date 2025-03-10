import os
import re
from datetime import datetime


from classes.Feeds import *


class FileProcessor:
    _DEFAULT_FILE = 'feeds.txt'
    VALID_TYPES = ('txt',)
    _VALID_FEEDS = (Feeds.News, Feeds.PrivateAd, Feeds.LuckyNumber)
    # _VALID_TYPES = ('txt', 'css', 'json', 'xml')

    _DEFAULT_FOLDER = 'default'
    _DEFAULT_DESTINATION_PATH = _DEFAULT_FOLDER + '/feeds.txt'
    _DEFAULT_PATH = _DEFAULT_FOLDER + '/info.'

    def __init__(self, path: str = None, type: str = 'txt'):
        if type not in FileProcessor.VALID_TYPES:
            raise TypeError(
                f"Unsupported file type '{type}'. Supported types are: {', '.join(FileProcessor.VALID_TYPES)}.")
        self._type = type

        self._path = path if path else f"{self._DEFAULT_PATH}{type}"

        self.ensure_default_files_and_folder_exist()
        self.ensure_file_exists()

    def __str__(self):
        return f"FileProcessor(path='{self._path}', type='{self._type}')"

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

    def append_all_feeds_from_file(self):
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


    # def remove_file(self._path):
    #     if os.path.exists(self._path):
    #         os.remove(self._path)

    # def read_from_file(file_path):
    #     if os.path.exists(file_path):
    #         with open(file_path, 'r') as file:
    #             return file.read()
    #     return None
    #
