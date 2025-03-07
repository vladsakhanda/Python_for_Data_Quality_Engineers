from Functions import str_to_date_format
from classes.LuckyNumber import LuckyNumber
from classes.News import News
from classes.PrivateAd import PrivateAd

objects = []

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
1. News
2. Private Ad
3. Lucky Number
4. News feed
    
You choose: ''')

    print('---\n')
    if user_input in ('1', 'News', '1. News'):
        news = News(input('You chose News! Enter news text: '),
                    input('Enter your city: '))
        print('\nThe next news were added:', news, end='\n\n')

        objects.append(news)

        is_exit = exit()

    elif user_input in ('2', 'Private Ad', '2. Private Ad'):
        text = input('You chose Private Ad! Enter private ad text: ')
        expiration_date = None

        while expiration_date is None:
            expiration_date = str_to_date_format(input('Enter expiration date in format "%d/%m/%Y": '),
                                                 PrivateAd.DATETIME_FORMAT)
            print(expiration_date)
            if expiration_date is not None:
                private_ad = PrivateAd(text, expiration_date)
                print('\nThe next private ad were added:', private_ad, end='\n\n')
                objects.append(private_ad)

                is_exit = exit()
            else:
                print('\nYour date is in the incorrect format.\n\n')
    elif user_input in ('3', 'Lucky Number', '3. Lucky Number'):
        lucky_number = LuckyNumber(input('You chose Lucky Number! Enter your name: '))
        print('\nThe next lucky number were added:', lucky_number, end='\n\n')

        objects.append(lucky_number)

        is_exit = exit()
    elif user_input in ('4', 'News feed', '4. News feed'):
        print('News feed:\n---')
        [print(object) for object in objects]
        print('---')

        is_exit = exit()
    else:
        print('No such option.', end=' ')

print('\nHave a nice day!')
