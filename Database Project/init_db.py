import psycopg2
import os
import csv 

# Connect to database
conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        password="UIS",
        port="5432")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create charging station table
cur.execute('''
    CREATE TABLE IF NOT EXISTS station (
        station_id VARCHAR(10) PRIMARY KEY,
        provider_name VARCHAR(100),
        address VARCHAR(100),
        station_latitude FLOAT,
        station_longitude FLOAT,
        price_no_subscription FLOAT,
        number_of_chargers INTEGER
    );
''')

# Create charging stand table
cur.execute('''
    CREATE TABLE IF NOT EXISTS charger (
        charger_id VARCHAR(10) PRIMARY KEY,
        station_id VARCHAR(10),
        type_1 INTEGER,
        type_2 INTEGER,
        ccs INTEGER,
        chademo INTEGER,
        charge_speed_type_1 FLOAT,
        charge_speed_type_2 FLOAT,
        charge_speed_ccs FLOAT,
        charge_speed_chademo FLOAT,
        availability INTEGER,
        FOREIGN KEY (station_id) REFERENCES station (station_id)
    );
''')

# Create user car info table
cur.execute('''
    CREATE TABLE IF NOT EXISTS car_info (
        car_info_id VARCHAR(20) PRIMARY KEY,
        type_1 INTEGER,
        type_2 INTEGER,
        ccs INTEGER,
        chademo INTEGER,
        travel_distance INTEGER,
        latitude FLOAT,
        longitude FLOAT
    );
''')

# Delete all data from tables, incase tables already have data
cur.execute('''
    TRUNCATE station, charger, car_info CASCADE;
    DELETE FROM station;
    DELETE FROM charger;
    DELETE FROM car_info;
''')

# Set user car info to default values
cur.execute('''
    INSERT INTO car_info (car_info_id, type_1, type_2, ccs, chademo, travel_distance, latitude, longitude)
    VALUES ('Genghis-Karen', 0, 0, 0, 0, 0, 0.0, 0.0);
''')

# Load data into station table
with open(os.path.join(os.getcwd(), 'station.csv'), 'r') as f:
    next(f) # Skip the header row.
    cur.copy_from(f, 'station', sep=',', columns=(
        'station_id',
        'provider_name',
        'address',
        'station_latitude',
        'station_longitude',
        'price_no_subscription',
        'number_of_chargers'
    ))

# Load data into charger table
with open(os.path.join(os.getcwd(), 'charger.csv'), 'r') as f:
    next(f) # Skip the header row.
    cur.copy_from(f, 'charger', sep=',', columns=(
        'charger_id',
        'station_id',
        'type_1',
        'type_2',
        'ccs',
        'chademo',
        'charge_speed_type_1',
        'charge_speed_type_2',
        'charge_speed_ccs',
        'charge_speed_chademo',
        'availability'
    ))

conn.commit()
cur.close()
conn.close()
