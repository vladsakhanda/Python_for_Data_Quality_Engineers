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
