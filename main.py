from classes.FileProcessor import FileProcessor
from classes.Functions import *
from classes.Feeds import Feeds


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
                    print('\nThe feed were added:', private_ad, end='\n\n')
                else:
                    print('\nYour date is in the incorrect format.\n\n')
        elif user_input in '3':
            name = input('You chose Lucky Number! Enter your name: ')
            lucky_number = Feeds.LuckyNumber(normalize_text(name))
            print('\nThe feed were added:', lucky_number, end='\n\n')

            FileProcessor().append_one_feed_to_file(lucky_number)
        elif user_input in ('4', 'Back'.upper(), '4, Back'.upper()):
            print()
        else:
            print('No such option.\n', end=' ')
            is_exit = False


def second_choice_flow():
    # is_exit = False
    # while not is_exit:
    #     is_exit = True
    print('---')
    print('2. Add feeds from one of the default files\n')

    file_type = choose_file_type()
    file_processor = FileProcessor(None, file_type)
    print(f"'{file_processor.get_path}' path and '{file_processor.get_type}' type have been chosen")

    file_processor.append_all_feeds_from_file()


def third_choice_flow():
    print('---')
    print('3. Add feeds from a specific file\n')

    file_type = choose_file_type()
    file_path = choose_file_path()

    file_processor = FileProcessor(file_path, file_type)
    print(f"'{file_processor.get_path}' path and '{file_processor.get_type}' type have been chosen")

    file_processor.append_all_feeds_from_file()


print('Hello!', end=' ')
is_exit_first_choices = False
while not is_exit_first_choices:
    user_input = input('''Choose one of the next options:
1. Add feeds using console
2. Add feeds from one of the default files
3. Add feeds from a specific file
4, Exit

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
                        'Exit'.upper(),
                        '4. Exit'.upper()):
        is_exit_first_choices = True
    else:
        print('No such option.', end=' ')

    print('---\n')

print('\nHave a nice day!')
