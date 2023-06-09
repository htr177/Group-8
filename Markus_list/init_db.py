import psycopg2
import csv as csv

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        password="ostehaps",
        port="1234")

# Open a cursor to perform database operations
cur = conn.cursor()


# Execute a command: this creates a new table
# Create Car/User table
# cur.execute('''
#     CREATE TABLE car (
#         car_id VARCHAR(10) PRIMARY KEY,
#         first_name VARCHAR(100),
#         last_name VARCHAR(100),
#         phone_number VARCHAR(15),
#         socket_type VARCHAR(10),
#         travel_distance INTEGER,
#         latitude FLOAT,
#         longitude FLOAT
#     );
# ''')

# # Create Charging Station table
# cur.execute('''
#     CREATE TABLE station (
#         station_id VARCHAR(10) PRIMARY KEY,
#         provider_name VARCHAR(100),
#         address VARCHAR(100),
#         station_latitude FLOAT,
#         station_longitude FLOAT,
#         price_no_subscription FLOAT,
#         number_of_chargers INTEGER
#     );
# ''')

# # Create Charging Stand table
# cur.execute('''
#     CREATE TABLE charger (
#         charger_id VARCHAR(10) PRIMARY KEY,
#         station_id VARCHAR(10),
#         type_1 INTEGER,
#         type_2 INTEGER,
#         ccs INTEGER,
#         chademo INTEGER,
#         charge_speed_type_1 FLOAT,
#         charge_speed_type_2 FLOAT,
#         charge_speed_ccs FLOAT,
#         charge_speed_chademo FLOAT,
#         availability INTEGER,
#         FOREIGN KEY (station_id) REFERENCES station (station_id)
#     );
# ''')

# cur.execute('''
#     CREATE TABLE car_info (
#         car_info_id VARCHAR(20) PRIMARY KEY,
#         type_1 INTEGER,
#         type_2 INTEGER,
#         ccs INTEGER,
#         chademo INTEGER,
#         travel_distance INTEGER,
#         latitude FLOAT,
#         longitude FLOAT
#     );
# ''')

cur.execute('''
    INSERT INTO car_info (car_info_id, type_1, type_2, ccs, chademo, travel_distance, latitude, longitude)
    VALUES ('Genghis-Karen', 0, 0, 0, 0, 0, 0.0, 0.0);
''')


# # Load data into Car/User table
# with open('C:/Users/marku/Desktop/DIS Project/car.csv', 'r') as f:
#     next(f) # Skip the header row.
#     cur.copy_from(f, 'car', sep=',', columns=(
#         'car_id',
#         'first_name',
#         'last_name',
#         'phone_number',
#         'socket_type',
#         'travel_distance',
#         'latitude',
#         'longitude'
#     ))

# # Load data into Charging Station table
# with open('C:/Users/marku/Desktop/DIS Project/station.csv', 'r') as f:
#     next(f) # Skip the header row.
#     cur.copy_from(f, 'station', sep=',', columns=(
#         'station_id',
#         'provider_name',
#         'address',
#         'station_latitude',
#         'station_longitude',
#         'price_no_subscription',
#         'number_of_chargers'
#     ))

# # Load data into Charging Stand table
# with open('C:/Users/marku/Desktop/DIS Project/charger.csv', 'r') as f:
#     next(f) # Skip the header row.
#     cur.copy_from(f, 'charger', sep=',', columns=(
#         'charger_id',
#         'station_id',
#         'type_1',
#         'type_2',
#         'ccs',
#         'chademo',
#         'charge_speed_type_1',
#         'charge_speed_type_2',
#         'charge_speed_ccs',
#         'charge_speed_chademo',
#         'availability'
#     ))

conn.commit()
cur.close()
conn.close()