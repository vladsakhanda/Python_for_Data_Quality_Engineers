from classes.FileProcessor import FileProcessor, DEFAULT_FILE
from Functions import str_to_date_format, normalize_text
from classes.Feeds import Feeds

FileProcessor.ensure_default_file_exists()
def exit():
    if input('Type \'E\' if you want to exit. Type anything if you want to add something else: ').upper() == 'E':
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
7, Exit

You choose: ''').upper()

    print('---\n')
    if user_input in ('1', 'News'.upper(), '1. News'.upper()):
        user_text = input('You chose News! Enter news text: ')
        city = input('Enter your city: ')
        news = Feeds.News(normalize_text(user_text), normalize_text(city))
        print('\nThe next news were added:', news, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(news))

        is_exit = exit()
    elif user_input in ('2', 'Private Ad'.upper(), '2. Private Ad'.upper()):
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

                is_exit = exit()
            else:
                print('\nYour date is in the incorrect format.\n\n')
    elif user_input in ('3', 'Lucky Number'.upper(), '3. Lucky Number'.upper()):
        name = input('You chose Lucky Number! Enter your name: ')
        lucky_number = Feeds.LuckyNumber(normalize_text(name))
        print('\nThe next lucky number were added:', lucky_number, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(lucky_number))

        is_exit = exit()
    elif user_input in ('4', 'Show news feed'.upper(), '4. Show news feed'.upper()):
        print('News feed (from default file):\n---')
        content = FileProcessor.read_from_file(DEFAULT_FILE)
        if content:
            print('News feed:\n---')
            print(content)
            print('---')
        else:
            print("No news feed available.")
    elif user_input in ('5', 'Show News feed from specific file'.upper(), '5. Show News feed from a specific file'.upper()):
        file_path = input('Enter the file path: ')
        content = FileProcessor.read_from_file(file_path)

        if content:
            print('News feed:\n---')
            print(content)
            print('---')
        else:
            print(f"No news feed available in {file_path}.")

        is_exit = exit()
    elif user_input in ('6', 'Add entries from a text file'.upper(), '6. Add entries from a text file'.upper()):
        file_path = input('Enter the file path of entries: ')
        content = normalize_text(FileProcessor.read_from_file(file_path))

        if content:
            FileProcessor.append_to_file(DEFAULT_FILE, content)
            FileProcessor.remove_file(file_path)
            print('\nEntries from the text file have been processed and added to the news feed.')
        else:
            print('File not found or empty.')

        is_exit = exit()
    elif user_input in ('7', 'Exit'.upper(), '7. Exit'.upper()):
        is_exit = True
    else:
        print('No such option.', end=' ')

print('\nHave a nice day!')
