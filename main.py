from Functions import str_to_date_format
from classes.Feeds import Feeds
from classes.FileProcessor import FileProcessor, DEFAULT_FILE

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
1. News
2. Private Ad
3. Lucky Number
4. Show news feed
    
You choose: ''')

    print('---\n')
    if user_input in ('1', 'News', '1. News'):
        user_text = input('You chose News! Enter news text: ')
        city = input('Enter your city: ')
        news = Feeds.News(user_text, city)
        print('\nThe next news were added:', news, end='\n\n')

        # objects.append(news)
        FileProcessor.append_to_file(DEFAULT_FILE, str(news))

        is_exit = exit()
    elif user_input in ('2', 'Private Ad', '2. Private Ad'):
        text = input('You chose Private Ad! Enter private ad text: ')
        expiration_date = None

        while expiration_date is None:
            date = input('Enter expiration date in format "%d/%m/%Y": ')
            expiration_date = str_to_date_format(date, Feeds.PrivateAd.DATETIME_FORMAT)
            print(expiration_date)
            if expiration_date:
                private_ad = Feeds.PrivateAd(text, expiration_date)
                print('\nThe next private ad were added:', private_ad, end='\n\n')
                # objects.append(private_ad)
                FileProcessor.append_to_file(DEFAULT_FILE, str(private_ad))

                is_exit = exit()
            else:
                print('\nYour date is in the incorrect format.\n\n')
    elif user_input in ('3', 'Lucky Number', '3. Lucky Number'):
        name = input('You chose Lucky Number! Enter your name: ')
        lucky_number = Feeds.LuckyNumber(name)
        print('\nThe next lucky number were added:', lucky_number, end='\n\n')

        # objects.append(lucky_number)
        FileProcessor.append_to_file(DEFAULT_FILE, str(lucky_number))

        is_exit = exit()
    elif user_input in ('4', 'Show news feed', '4. Show news feed'):
        print('News feed:\n---')
        print(FileProcessor.read_from_file(DEFAULT_FILE))
        print('---')

        is_exit = exit()
    else:
        print('No such option.', end=' ')

print('\nHave a nice day!')
