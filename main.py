from FileProcessor import FileProcessor, DEFAULT_FILE
from Functions import str_to_date_format, normalize_text
from classes.LuckyNumber import LuckyNumber
from classes.News import News
from classes.PrivateAd import PrivateAd

objects = []
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
6. Add entries from a text file
7, Exit

You choose: ''')

    print('---\n')
    if user_input in ('1', 'News', '1. News'):
        news = News(normalize_text(input('You chose News! Enter news text: ')),
                    normalize_text(input('Enter your city: ')))
        print('\nThe next news were added:', news, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(news))

        objects.append(news)

        is_exit = exit()

    elif user_input in ('2', 'Private Ad', '2. Private Ad'):
        text = normalize_text(input('You chose Private Ad! Enter private ad text: '))
        expiration_date = None

        while expiration_date is None:
            expiration_date = str_to_date_format(input('Enter expiration date in format "%d/%m/%Y": '),
                                                 PrivateAd.DATETIME_FORMAT)
            print(expiration_date)
            if expiration_date is not None:
                private_ad = PrivateAd(text, expiration_date)
                print('\nThe next private ad were added:', private_ad, end='\n\n')

                FileProcessor.append_to_file(DEFAULT_FILE, str(private_ad))
                objects.append(private_ad)

                is_exit = exit()
            else:
                print('\nYour date is in the incorrect format.\n\n')
    elif user_input in ('3', 'Lucky Number', '3. Lucky Number'):
        lucky_number = LuckyNumber(normalize_text(input('You chose Lucky Number! Enter your name: ')))
        print('\nThe next lucky number were added:', lucky_number, end='\n\n')

        FileProcessor.append_to_file(DEFAULT_FILE, str(lucky_number))
        objects.append(lucky_number)

        is_exit = exit()
    elif user_input in ('4', 'News feed', '4. News feed'):
        print('News feed (from default file):\n---')
        content = FileProcessor.read_from_file(DEFAULT_FILE)
        if content:
            print(content)
        else:
            print("No news feed available.")
        print('---')

        is_exit = exit()
    elif user_input in ('5', 'Show News feed from specific file', '5. Show News feed from a specific file'):
        file_path = input('Enter the file path: ')

        content = FileProcessor.read_from_file(file_path)
        if content:
            print(content)
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
            print('\nEntries from the text file have been processed and added to the news feed.')
        else:
            print('File not found or empty.')

        is_exit = exit()
    elif user_input in ('7', 'Exit', '7. Exit'):
        is_exit = True
    else:
        print('No such option.', end=' ')

print('\nHave a nice day!')
