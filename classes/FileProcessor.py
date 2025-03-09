import os

DEFAULT_FILE = 'default_news_feed.txt'
DEFAULT_JSON_FILE = 'default_news_feed.json'

class FileProcessor:

    @staticmethod
    def ensure_default_file_exists():
        if not os.path.exists(DEFAULT_FILE):
            with open(DEFAULT_FILE, 'w') as f:
                f.write('')

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def read_from_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        return None

    @staticmethod
    def append_to_file(file_path, content):
        with open(file_path, 'a') as file:
            file.write(content + "\n")