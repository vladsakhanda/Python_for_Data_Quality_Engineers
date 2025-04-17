import json
import os
from datetime import datetime

from classes.FileProcessor import FileProcessor


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

    make_upper_case_next_word = True
    for symbol in text:
        if make_upper_case_next_word and symbol.isalpha():
            symbol = symbol.upper()
            make_upper_case_next_word = False
        if symbol in ('.', ';', ':'):
            make_upper_case_next_word = True

        new_text += symbol

    return new_text


@DeprecationWarning
def exit():
    if input('Type \'E\' if you want to exit. Type anything if you want to add something else: ').upper() == 'E':
        print()
        return True
    else:
        return False


def choose_file_type():
    """Prompt the user to choose a valid file type from a predefined list.

        The function repeatedly asks for input until a valid file type is selected.
        Valid file types are defined within the function as ('txt', 'css', 'json', 'xml').

        Returns:
            str: The chosen file type, which is guaranteed to be valid.

        Raises:
            None.
    """
    while True:
        file_type = input(f"Supported types are: {FileProcessor.VALID_TYPES}. Choose file type: ").strip()

        if file_type not in FileProcessor.VALID_TYPES:
            print(f"\nInvalid input. Supported types are: {FileProcessor.VALID_TYPES}.\n")
            continue

        print(f"{file_type} type has been chosen.\n")

        return file_type


def choose_file_path():
    while True:
        file_path = input(f"Enter the path to your file: ").strip()

        if not os.path.isfile(file_path):
            print("\nThe file doesn't exist or the path is incorrect. Please try again.\n")
            continue

        print(f"\nFile path '{file_path}'  type has been chosen.")

        return file_path


def create_test_files():
    """
    Ensures the required files exist with specific content in the current folder.
    Creates only the files: 1.txt, 1.csv, 1.json, and 1.xml.
    """
    # Define file content templates
    files_content = {
        "1.csv": "News, Vlad, Kyiv",
        "1.json": json.dumps([
            {
                "type": "news",
                "text": "Vlad",
                "city": "Kyiv"
            },
            {
                "type": "lucky_number",
                "name": "Vlad"
            },
            {
                "type": "private_ad",
                "text": "Buy one, get one free!",
                "expiration_date": "15/10/2023"
            }
        ], indent=2),
        "1.txt": """News, Vlad, Kyiv
Lucky Number, Vlad
Private Add, I love Ukraine, 05/05/2025""",
        "1.xml": """<feeds>
    <feed type="news">
        <text>Breaking news: Python is awesome!</text>
        <city>San Francisco</city>
    </feed>
    <feed type="lucky_number">
        <name>Alice</name>
        <lucky_number>42</lucky_number>
    </feed>
    <feed type="private_ad">
        <text>Buy one, get one free!</text>
        <expiration_date>15/10/2023</expiration_date>
    </feed>
</feeds>"""
    }

    # Iterate through the defined files and their content
    for file_name, content in files_content.items():
        # Check if the file already exists
        if not os.path.exists(file_name):
            # Write the specified content into the file
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(content)
                print(f"Created file: {file_name}")
        else:
            print(f"File already exists: {file_name}")
