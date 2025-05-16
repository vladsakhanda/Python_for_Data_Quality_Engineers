import DBManagement

is_exit = False
while not is_exit:
    show_distance = True
    first_city = input('''Type 1 to exit. Or enter the first city name: ''')

    if first_city == '1':
        break

    if not DBManagement.does_city_exist(first_city):

        if input('\nType 1 to add this city to the database. Type anything else to skip: ') == '1':
            try:
                latitude = float(input('Enter latitude: '))
                longitude = float(input('Enter longitude: '))
            except ValueError:
                print('Latitude and longitude have to be numerical.\n')
                continue
            DBManagement.add_city_to_DB(first_city, latitude, longitude)
        else:
            show_distance = False

    second_city = input('''\nType 1 to exit. Or enter the second city name: ''')

    if second_city == '1':
        break

    if not DBManagement.does_city_exist(second_city):
        if input('\nType 1 to add this city to the database. Type anything else to skip: ') == '1':
            try:
                latitude = float(input('Enter latitude: '))
                longitude = float(input('Enter longitude: '))
            except ValueError:
                print('Latitude and longitude have to be numerical.\n')
                continue
            DBManagement.add_city_to_DB(second_city, latitude, longitude)
        else:
            show_distance = False

    if show_distance:
        print(f'\nDistance between {first_city} and {second_city} in kilometers:',
              DBManagement.distance_between_cities_in_km(first_city, second_city))

    print('\n---')