from datetime import datetime
import csv
import re
from collections import Counter


def str_to_date_format(date: str, date_format: str):
    """
    Takes date and converts to taken data_format
    If date is in incorrect format, the function returns: None
    :param date: str
    :return: datetime
    """
    try:
        return datetime.strptime(date, date_format)
    except ValueError or TypeError:
        return None

def normalize_text(text: str):
    new_text = ''
    number_of_whitespace_characters = 0

    make_upper_case_next_word = True
    for symbol in text:
        if symbol.isspace():
            number_of_whitespace_characters += 1

        if make_upper_case_next_word and symbol.isalpha():
            symbol = symbol.upper()
            make_upper_case_next_word = False
        if symbol in ('.', ';', ':'):
            make_upper_case_next_word = True

        new_text += symbol

    return new_text

def csv_parsing(default_file_path: str):
    with open(default_file_path, "r") as file:
        text = file.read()

    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    with open("word_count.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            writer.writerow([word, count])

    letters = [char for char in text if char.isalpha()]
    letter_counts = Counter(letters)
    uppercase_counts = Counter(c for c in text if c.isupper())
    total_letters = sum(letter_counts.values())
    with open("letter_count.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
        for letter, count in sorted(letter_counts.items()):
            uppercase_count = uppercase_counts.get(letter.upper(), 0)
            percentage = (count / total_letters) * 100
            writer.writerow([letter, count, uppercase_count, f"{percentage:.2f}"])