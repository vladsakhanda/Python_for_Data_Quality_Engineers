from datetime import datetime


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
