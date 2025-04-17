from classes import DBManagement
from classes.Feeds import Feeds
from classes.Functions import *


def first_choice_flow():
    is_exit = False
    while not is_exit:
        is_exit = True
        print('---')
        print('Your choice: 1. Add feeds using console\n')

        user_input = input('''Choose one of the next options:
1. Add News to the 'result.txt' file
2. Add Private Ad the 'result.txt' file
3. Add Lucky Number the 'result.txt' file
4, Back
    
You choose: ''').upper()

        if user_input in '1':
            user_text = input('You chose News! Enter news text: ')
            city = input('Enter your city: ')
            news = Feeds.News(normalize_text(user_text), normalize_text(city))
            print('\nThe feed were added:', news, end='\n\n')

            FileProcessor().append_one_feed_to_file(news)
            FileProcessor().save_one_feed_to_db(news)
        elif user_input in '2':
            text = normalize_text(input('You chose Private Ad! Enter private ad text: '))
            expiration_date = None

            while expiration_date is None:
                date = input('Enter expiration date in format "%d/%m/%Y": ')
                expiration_date = str_to_date_format(date, Feeds.PrivateAd.DATETIME_FORMAT)
                print(expiration_date)
                if expiration_date:
                    private_ad = Feeds.PrivateAd(text, expiration_date)
                    FileProcessor().append_one_feed_to_file(private_ad)
                    FileProcessor().save_one_feed_to_db(private_ad)
                    print('\nThe feed were added:', private_ad, end='\n\n')
                else:
                    print('\nYour date is in the incorrect format.\n\n')
        elif user_input in '3':
            name = input('You chose Lucky Number! Enter your name: ')
            lucky_number = Feeds.LuckyNumber(normalize_text(name))
            print('\nThe feed were added:', lucky_number, end='\n\n')

            FileProcessor().append_one_feed_to_file(lucky_number)
            FileProcessor().save_one_feed_to_db(lucky_number)
        elif user_input in ('4', 'Back'.upper(), '4, Back'.upper()):
            print()
        else:
            print('No such option.\n', end=' ')
            is_exit = False


def second_choice_flow():
    print('---')
    print('2. Add feeds from one of the default files\n')

    file_type = choose_file_type()

    file_processor = FileProcessor(None, file_type)
    print(f"'{file_processor.get_path}' path and '{file_processor.get_type}' type have been chosen")
    file_processor.append_all_feeds_from_file()
    # FileProcessor().save_one_feed_to_db(lucky_number)

def third_choice_flow():
    print('---')
    print('3. Add feeds from a specific file\n')

    while True:
        try:
            file_path = choose_file_path()
            file_processor = FileProcessor(file_path)
            print(f"'{file_processor.get_path}' path and '{file_processor.get_type}' type have been chosen")
            file_processor.append_all_feeds_from_file()
            break
        except TypeError as e:
            print(e, end='\n\n')


def fourth_choice_flow():
    is_exit = False
    while not is_exit:
        print('---')
        print('Your choice: 4. Calculate distance between two cities\n')

        first_city = input('''Enter the first city name: ''')
        if not DBManagement.does_city_exist(first_city):
            if input('\nType 1 to add this city to the database. Type anything else to skip: ') == '1':
                latitude = float(input('Enter latitude: '))
                longitude = float(input('Enter longitude: '))
                DBManagement.add_city_to_DB(first_city, latitude, longitude)


            if input('\nType 1 to move back. Type anything else to continue: ') == '1':
                break

        second_city = input('''\nEnter the second city name: ''')
        if not DBManagement.does_city_exist(second_city):
            if input('\nType 1 to add this city to the database. Type anything else to skip: ') == '1':
                latitude = float(input('Enter latitude: '))
                longitude = float(input('Enter longitude: '))
                DBManagement.add_city_to_DB(second_city, latitude, longitude)

            if input('\nType 1 to move back. Type anything else to continue: ') == '1':
                break

        if DBManagement.does_city_exist(first_city) or DBManagement.does_city_exist(second_city):
            print(f'Distance between {first_city} and {second_city} in kilometers:', DBManagement.distance_between_cities_in_km(first_city, second_city))

        if input('\nType 1 to move back. Type anything else to continue: ') == '1':
            break



print('Hello!', end=' ')
is_exit_first_choices = False
while not is_exit_first_choices:
    user_input = input('''Choose one of the next options:
1. Add feeds using console
2. Add feeds from one of the default files
3. Add feeds from a specific file
4. Calculate distance between two cities
5, Exit

You choose: ''').upper()

    if user_input in ('1',
                      'Add feeds using console'.upper(),
                      '1. Add feeds using console'.upper()):
        first_choice_flow()
    elif user_input in ('2',
                        'Add feeds from one of the default files'.upper(),
                        '2. Add feeds from one of the default files'.upper()):
        second_choice_flow()
    elif user_input in ('3',
                        'Add feeds from a specific file'.upper(),
                        '3. Add feeds from a specific file'.upper()):
        third_choice_flow()
    elif user_input in ('4',
                        'Calculate distance between two cities'.upper(),
                        '4. Add feeds from a specific file'.upper()):
        fourth_choice_flow()
    elif user_input in ('5',
                        'Exit'.upper(),
                        '5. Exit'.upper()):
        is_exit_first_choices = True
    else:
        print('No such option.', end=' ')

    print('---\n')

print('\nHave a nice day!')
