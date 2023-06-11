from flask import Flask, render_template, flash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import psycopg2.extras
from geopy.distance import geodesic

## APP SETUP ##
app = Flask(__name__, template_folder="templates") 
app.secret_key = 'some_secret'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCtzTSyDxwFhEfsyJazopYkbXmIehHXVTM" 
GoogleMaps(app)

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        #password="postgres",
        port="5432")


curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

## ROUTES ##
@app.route('/map', methods=['GET', 'POST']) 
def mapview():
    # Extract coordinates from database
    curr.execute("SELECT station_latitude, station_longitude, address, provider_name FROM station")
    rows = curr.fetchall()
    curr.execute("SELECT latitude, longitude FROM car_info")
    car = curr.fetchone()
    # Add to markers list
    mymap = Map(
        identifier="view-side", 
        lat=55.867037,
        lng=10.596938,
        zoom=10.2,
        style="height:500px;width:1050px;margin:0;",
        markers=[{'icon' : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png', 
                  'lat' : row['station_latitude'], 
                  'lng' : row['station_longitude'], 
                  'infobox': '<b>' + row['provider_name'] + '</b> <br>' + '<b>' + 'Address:' + '</b>' + row['address'] + '<br>' 
                  + '<a href=' + 'https://www.google.com/maps/dir/' + str(car['latitude']) + ',' + str(car['longitude']) 
                  + '/' + str(row['station_latitude']) + ',' + str(row['station_longitude']) 
                  + '> click for directions! </a>'} for row in rows
                  ] +
                  [{'icon' : 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', 
                    'lat' : car['latitude'], 
                    'lng' : car['longitude']}]        
    )

    return render_template('map.html', mymap=mymap)


@app.route('/list', methods=['GET', 'POST'])
def listview():
    # the car's requirements and location
    curr.execute("SELECT * FROM car_info WHERE car_info_id = %s", ('Genghis-Karen',))
    car_info = curr.fetchone()

    # SQL query
    sql_query = """
        SELECT s.station_id, s.provider_name, s.address, s.station_latitude, s.station_longitude, 
            c.charger_id, c.availability, c.type_1, c.type_2, c.ccs, c.chademo, c.charge_speed_type_1, c.charge_speed_type_2, c.charge_speed_ccs, c.charge_speed_chademo, s.price_no_subscription,
            {distance} as distance 
        FROM station s
        INNER JOIN charger c ON s.station_id = c.station_id
        WHERE 
            ((c.type_1 = %s OR c.type_2 = %s OR c.ccs = %s OR c.chademo = %s) AND c.availability = 1 AND %s > 0)

        ORDER BY distance
    """

    # Calculate the distance and convert it to a float
    distance = geodesic(
        (float(car_info['latitude']), float(car_info['longitude'])),
        (float(car_info['latitude']), float(car_info['longitude']))
    ).km

    # Add travel distance calculation to the SQL query
    sql_query = sql_query.format(distance=distance)

    params = (
        car_info['type_1'], car_info['type_2'], car_info['ccs'], car_info['chademo'],
        car_info['travel_distance']
    )

    # Execute the SQL query
    curr.execute(sql_query, params)
    result = curr.fetchall()

    # Calculate the distance for each charger and convert it to a float
    chargers = []
    for row in result:
        charger_latitude = float(row['station_latitude'])
        charger_longitude = float(row['station_longitude'])
        charger_distance = geodesic(
            (float(car_info['latitude']), float(car_info['longitude'])),
            (charger_latitude, charger_longitude)
        ).km
        
     
        # Add the charger information and distance to the list
        chargers.append({
            'station_id': row['station_id'],
            'provider_name': row['provider_name'],
            'address': row['address'],
            'charger_id': row['charger_id'],
            'availability': row['availability'],
            'distance': round(charger_distance, 2),
            'type_1': row['type_1'] if row['type_1'] == 1 else '-',
            'type_2': row['type_2'] if row['type_2'] == 1 else '-',
            'ccs': row['ccs'] if row['ccs'] == 1 else '-',
            'chademo': row['chademo'] if row['chademo'] == 1 else '-',
            'charge_speed_type_1': row['charge_speed_type_1'] if row['type_1'] == 1 else '-',
            'charge_speed_type_2': row['charge_speed_type_2'] if row['type_2'] == 1 else '-',
            'charge_speed_ccs': row['charge_speed_ccs'] if row['ccs'] == 1 else '-',
            'charge_speed_chademo': row['charge_speed_chademo'] if row['chademo'] == 1 else '-',
            'price_no_subscription': row['price_no_subscription']
        })

    chargers = [charger for charger in chargers if charger['availability'] == 1]
    chargers = [charger for charger in chargers if charger['distance'] <= car_info['travel_distance']]
    chargers = [charger for charger in chargers if charger['type_1'] == car_info['type_1'] == 1 or charger['type_2'] == car_info['type_2'] == 1 or charger['ccs'] == car_info['ccs'] == 1 or charger['chademo'] == car_info['chademo'] == 1]
    
    # Sort the chargers by distance
    chargers = sorted(chargers, key=lambda k: k['distance'])

    # Return the list of chargers
    return render_template('list.html', chargers=chargers)


@app.route('/')
def home():
    return render_template ('homepage.html')


@app.route('/form', methods=['GET', 'POST'])
def fill():
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        travel_distance = int(request.form['travel_dis'])
        print(latitude)
        curr.execute("UPDATE car_info SET latitude = %s, longitude = %s, travel_distance = %s WHERE car_info_id = %s", (latitude, longitude, travel_distance, 'Genghis-Karen'))
        conn.commit()
        return redirect(url_for('mapview'))
    return render_template ('form2.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        sockets = {'Type 1' : 0, 'Type 2' : 0, 'CCS' : 0, 'CHA' : 0}
        checkbox_values = request.form.getlist('check')
        for i in checkbox_values:
            if i == 'Type 1':
                sockets['Type 1'] = 1
            elif i == 'Type 2':
                sockets['Type 2'] = 1
            elif i == 'CCS':
                sockets['CCS'] = 1
            elif i == 'CHA':
                sockets['CHA'] = 1
        type_1 = sockets['Type 1']
        type_2 = sockets['Type 2']
        CCS = sockets['CCS']
        CHA = sockets['CHA']

        curr.execute("UPDATE car_info SET type_1 = %s, type_2 = %s, ccs = %s, chademo = %s WHERE car_info_id = %s", (type_1, type_2, CCS, CHA, 'Genghis-Karen'))
        conn.commit()
        flash('Car information added successfully')
        return redirect(url_for('fill'))
    return render_template('form1.html')

if __name__ == "__main__":
    app.run(debug=True)