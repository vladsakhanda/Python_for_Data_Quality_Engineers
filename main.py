from classes.Feeds import Feeds
from classes.FileProcessor import FileProcessor, DEFAULT_FILE, DEFAULT_JSON_FILE
from classes.Functions import str_to_date_format, normalize_text, csv_parsing
from classes.JsonProcessing import json_reader, create_default_JSON_file

FileProcessor.ensure_default_file_exists()


def exit():
    if input('Type \'E\' if you want to exit. Type anything if you want to add something else: ') == 'E':
        print()
        return True
    else:
        return False


print('Hello!', end=' ')
is_exit = False
while not is_exit:
    user_input = input('''Choose one of the next options to add:
1. Add News to default file
2. Add Private Ad to default file
3. Add Lucky Number to default file
4. Show News feed from default file
5. Show News feed from a specific file
6. Add entries from a text file to default file
7. Add entries from a JSON file to default file
8. Exit

You choose: ''')

    print('---\n')
    if user_input in ('1', 'News', '1. News'):
        user_text = input('You chose News! Enter news text: ')
        city = input('Enter your city: ')
        news = Feeds.News(normalize_text(user_text), normalize_text(city), None)
        print('\nThe next news were added:', news, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(news))
        csv_parsing(DEFAULT_FILE)
        create_default_JSON_file(DEFAULT_FILE, DEFAULT_JSON_FILE)

        is_exit = exit()
    elif user_input in ('2', 'Private Ad', '2. Private Ad'):
        text = normalize_text(input('You chose Private Ad! Enter private ad text: '))
        expiration_date = None

        while expiration_date is None:
            date = input('Enter expiration date in format "%d/%m/%Y": ')
            expiration_date = str_to_date_format(date, Feeds.PrivateAd.DATETIME_FORMAT)
            print(expiration_date)
            if expiration_date:
                private_ad = Feeds.PrivateAd(text, expiration_date)
                print('\nThe next private ad were added:', private_ad, end='\n\n')
                FileProcessor.append_to_file(DEFAULT_FILE, str(private_ad))
                csv_parsing(DEFAULT_FILE)
                create_default_JSON_file(DEFAULT_FILE, DEFAULT_JSON_FILE)

                is_exit = exit()
            else:
                print('\nYour date is in the incorrect format.\n\n')
    elif user_input in ('3', 'Lucky Number', '3. Lucky Number'):
        name = input('You chose Lucky Number! Enter your name: ')
        lucky_number = Feeds.LuckyNumber(normalize_text(name))
        print('\nThe next lucky number were added:', lucky_number, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(lucky_number))
        csv_parsing(DEFAULT_FILE)
        create_default_JSON_file(DEFAULT_FILE, DEFAULT_JSON_FILE)

        is_exit = exit()
    elif user_input in ('4', 'Show news feed', '4. Show news feed'):
        print('News feed (from default file):\n---')
        content = FileProcessor.read_from_file(DEFAULT_FILE)
        if content:
            print('News feed:\n---')
            print(normalize_text(content))
            print('---')
        else:
            print("No news feed available.")
        is_exit = exit()
    elif user_input in ('5', 'Show News feed from specific file', '5. Show News feed from a specific file'):
        file_path = input('Enter the file path: ')
        content = ''
        if file_path.endswith('.json'):
            content = '\n'.join(str(obj) for obj in json_reader(file_path))
        else:
            content = FileProcessor.read_from_file(file_path)

        if content:
            print('News feed:\n---')
            print(normalize_text(content))
            print('---')
        else:
            print(f"No news feed available in {file_path}.")
        print('---')

        is_exit = exit()
    elif user_input in ('6', 'Add entries from a text file', '6. Add entries from a text file'):
        file_path = input('Enter the file path of entries: ')
        content = normalize_text(FileProcessor.read_from_file(file_path))

        if content:
            FileProcessor.append_to_file(DEFAULT_FILE, content)
            FileProcessor.remove_file(file_path)
            csv_parsing(DEFAULT_FILE)
            create_default_JSON_file(DEFAULT_FILE, DEFAULT_JSON_FILE)
            print('\nEntries from the text file have been processed and added to the news feed.')
        else:
            print('File not found or empty.')
        is_exit = exit()
    elif user_input in ('7', 'Add entries from a JSON file to default file', '7. Add entries from a JSON file to default file'):
        file_path = input('Enter the file path of entries: ')
        content = json_reader(file_path)
        if file_path.endswith('.json') and content:
            content = '\n'.join(str(obj) for obj in json_reader(file_path))

            FileProcessor.append_to_file(DEFAULT_FILE, normalize_text(content))
            FileProcessor.remove_file(file_path)
            csv_parsing(DEFAULT_FILE)
            create_default_JSON_file(DEFAULT_FILE, DEFAULT_JSON_FILE)
            print('\nEntries from the JSON file have been processed and added to the news feed.\n')
        else:
            print('File not found or it is not a JSON file.\n')

    elif user_input in ('8', 'Exit', '8. Exit'):
        is_exit = True
    else:
        print('No such option.', end=' ')

print('\nHave a nice day!')
