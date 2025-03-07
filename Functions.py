from datetime import datetime


def str_to_date_format(date: str, date_format: str):
    """
    Takes date and converts to taken data_format.
    If date is in incorrect format, the function returns: None
    :param date: str
    :return: datetime
    """
    try:
        return datetime.strptime(date, date_format)
    except ValueError or TypeError:
        return None

