import math
import sqlite3

connection = sqlite3.connect("cities.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(50) UNIQUE NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);
""")

def does_city_exist(city_name : str):
    cursor.execute("""
    SELECT * FROM cities
    WHERE city = ?;
    """, (city_name,))

    result = cursor.fetchone()

    if result:
        print(f"City '{city_name}' exists in the database: {result}")
        return True
    else:
        print(f"City '{city_name}' does not exist in the database.")
        return False

def add_city_to_DB (city_name : str, latitude : float, longitude: float):
    try:
        cursor.execute("""
            INSERT INTO cities (city, latitude, longitude)
            VALUES (?, ?, ?);
            """, (city_name, latitude, longitude))
        connection.commit()  # Commit every time we make changes
        print(f"City '{city_name}' is successfully added to database with {latitude} latitude and {longitude} longitude.")
    except sqlite3.IntegrityError:
        print(f"City '{city_name}' already exists in the database.")


def distance_between_cities_in_km(first_city, second_city):
    """
    Calculate the great-circle distance between two points on the Earth using the Haversine formula.

    Returns:
        Distance between the two points in kilometers.
    """
    cursor.execute("""
            SELECT latitude, longitude
            FROM cities
            WHERE city = ?;
        """, (first_city,))
    first_city_coordinates = cursor.fetchone()

    if not first_city_coordinates:
        print(f"City '{first_city}' not found in the database.")
        return None

    latitude_1, longitude_1 = first_city_coordinates

    cursor.execute("""
            SELECT latitude, longitude
            FROM cities
            WHERE city = ?;
        """, (second_city,))
    second_city_coordinates = cursor.fetchone()

    if not second_city_coordinates:
        print(f"City '{second_city}' not found in the database.")
        return None

    latitude_2, longitude_2 = second_city_coordinates

    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitudes and longitudes from degrees to radians
    lat1, lon1 = math.radians(latitude_1), math.radians(longitude_1)
    lat2, lon2 = math.radians(latitude_2), math.radians(longitude_2)

    # Differences in latitude and longitude
    diff_latitude = lat2 - lat1
    diff_longitude = lon2 - lon1

    # Haversine formula
    a = math.sin(diff_latitude / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance

