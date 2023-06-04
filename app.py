# from flask import Flask, render_template
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map

# #app = Flask(__name__) 
# #app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"

# #GoogleMaps(app)

# # you can also pass the key here if you prefer
# #GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")

# #@app.route('/')
# #def home():
#   #  return render_template('please.html') 
# #if __name__ == '__main__':
#  #   app.run(debug=True)

# app = Flask(__name__) #template_folder="."
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyAzeggzDErZuRAL6B4P1eIOxiYZouYLxu8" 
# GoogleMaps(app)

# #@app.route("/")
# #def mapview():
# #    return render_template('index.html')

# @app.route("/")
# def mapview():
#     # creating a map in the view
#     mymap = Map(
#         identifier="view-side",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[(37.4419, -122.1419)]
#     )
#     sndmap = Map(
#         identifier="sndmap",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#              'lat': 37.4419,
#              'lng': -122.1419,
#              'infobox': "<b>Hello World</b>"
#           },
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
#              'lat': 37.4300,
#              'lng': -122.1400,
#              'infobox': "<b>Hello World from other place</b>"
#           }
#         ]
#     )
#     return render_template('index.html', mymap=mymap, sndmap=sndmap)

# if __name__ == "__main__":
#     app.run(debug=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
# require Flask-GoogleMaps (https://github.com/rochacbruno/Flask-GoogleMaps)

app = Flask(__name__)
api_key = 'AIzaSyAzeggzDErZuRAL6B4P1eIOxiYZouYLxu8' # change this to your api key
# get api key from Google API Console (https://console.cloud.google.com/apis/)
GoogleMaps(app, key=api_key) # set api_key
devices_data = {} # dict to store data of devices
devices_location = {} # dict to store coordinates of devices
# use sqlalchemy or something to store things in database

@app.route('/', methods=['GET', 'POST'])
def index():
    # json_data = request.get_json(silent=True)
    # get json request

    json_data = { # for testing
        'user' : {
            'x' : 37.50611,
            'y' : 127.0616346
        },
        'devices' : [
            {
                'id' : '0001',
                'x' : 37.5077121,
                'y' : 127.0624397,
                'data' : 'something'
            }
        ]
    }

    user_location = (json_data['user']['x'], json_data['user']['y'])
    # json example : { 'user' : { 'x' : '300' , 'y' : '300' } }
    # get user_location from json & store as turple (x, y)

    devices_data[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['data']
    )

    devices_location[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['x'], 
        json_data['devices'][0]['y']
    )
    # json example : { 'devices' : { 'id' : '0001', x' : '500', 'y' : '500' }, { ... } }
    # get device_location from json & store turple (x, y) in dictionary with device id as key
    # use for statements or something to get more locations from more devices

    circle = { # draw circle on map (user_location as center)
        'stroke_color': '#0000FF',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        # line(stroke) style
        'fill_color': '#FFFFFF', 
        'fill_opacity': .2,
        # fill style
        'center': { # set circle to user_location
            'lat': user_location[0],
            'lng': user_location[1]
        }, 
        'radius': 500 # circle size (50 meters)
    }

    map = Map(
        identifier = "map", varname = "map",
        # set identifier, varname
        lat = user_location[0], lng = user_location[1], 
        # set map base to user_location
        zoom = 15, # set zoomlevel
        markers = [
            {
                'lat': devices_location['0001'][0],
                'lng': devices_location['0001'][1],
                'infobox': devices_data['0001']
            }
        ], 
        # set markers to location of devices
        circles = [circle] # pass circles
    )

    return render_template('maps.html', map=map) # render template

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    json_data = requests.get.args('json')
    return json_data
    # you can use this to get request with strings and parse json
    # put data in database or something

if __name__ == '__main__':
    app.run(debug = True) # run app