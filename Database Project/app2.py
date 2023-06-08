from flask import Flask, render_template, flash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import psycopg2.extras
import uuid



app = Flask(__name__, template_folder="templates") 
app.secret_key = 'some_secret'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCtzTSyDxwFhEfsyJazopYkbXmIehHXVTM"
GoogleMaps(app)

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        password="ostehaps",
        port="1234")


curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


@app.route('/map', methods=['GET', 'POST']) 
def mapview():
    # Extract coordinates from database
    curr.execute("SELECT station_latitude, station_longitude, address, provider_name FROM station")
    rows = curr.fetchall()
    curr.execute("SELECT latitude, longitude FROM car_info")
    car = curr.fetchone()
    print(rows)
    # Add to markers list
    mymap = Map(
        identifier="view-side",
        lat=55.827037,
        lng=10.596938,
        zoom=10,
        style="height:500px;width:800px;margin:0;",
        markers=[{'icon' : 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 
                  'lat' : row['station_latitude'], 
                  'lng' : row['station_longitude'], 
                  'infobox': '<b>' + row['provider_name'] + '</b> <br>' + '<b>' + 'address:' + '</b>' + row['address'] + '<br>' 
                  + '<a href=' + 'https://www.google.com/maps/dir/' + str(car['latitude']) + ',' + str(car['longitude']) 
                  + '/' + str(row['station_latitude']) + ',' + str(row['station_longitude']) 
                  + '> click for directions! </a>'} for row in rows
                  ] +
                  [{'icon' : 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', 
                    'lat' : car['latitude'], 
                    'lng' : car['longitude']}]        
    )
    # make the address unicode
    # address = address.encode('utf-8')

    return render_template('map.html', mymap=mymap)

@app.route('/list', methods=['GET', 'POST'])
def listview():
    curr.execute("SELECT * FROM charger WHERE availability = 1 AND ")
    return render_template('list.html')

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

@app.route('/user/user/Karen')
def go_back():
    return redirect(url_for('user', name='Karen'))


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
        #random unique id length 10

        car_id = str(uuid.uuid4().hex[:10].upper())
        curr.execute("UPDATE car_info SET type_1 = %s, type_2 = %s, ccs = %s, chademo = %s WHERE car_info_id = %s", (type_1, type_2, CCS, CHA, 'Genghis-Karen'))
        conn.commit()
        flash('Car information added successfully')
        # return render_template(fill.html)
        # Print the form data to the console
        # for key, value in request.form.items():
        #     print(f'{key}: {value}')
        #return render_template('form2.html')
        return redirect(url_for('fill'))
    
    return render_template('form1.html')

if __name__ == "__main__":
    app.run(debug=True)