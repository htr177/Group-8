# from flask import Flask, render_template
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
import json
import requests
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
#from flask_googlemaps import GoogleMaps, Map


from pydantic import BaseModel, validator


app = Flask(__name__)


# "https://1.bp.blogspot.com/-sTxAHAxirGM/WVbAe2098nI/AAAAAAABENs/_I5sYMYgLOUzaIE7FfF4qdGX-hoAkq9SgCLcBGAs/s1600/Blog_20170624_113552.jpg"

######################
#app.register_blueprint(views, url_prefix="/")
@app.route('/')
def home():
    return render_template ('hej.html')

@app.route('/form', methods=['GET', 'POST'])
def fill():
    return render_template ('fill.html')

@app.route('/user/user/Karen')
def go_back():
    return redirect(url_for('user', name='Karen'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        print(request.form.getlist('check'))
        # return render_template(fill.html)
        # Print the form data to the console
        # for key, value in request.form.items():
        #     print(f'{key}: {value}')
    return render_template('please.html')



# access json
@app.route("/json")
def get_json():
    return jsonify({"name": "Tim", 'age': 21, 'hobbies': ['coding', 'reading', 'gaming']})

# access data from json
@app.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@app.route("/go-to-home")
def go_to_home():
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)




######################## GOOGLE MAPS - virker ik ##########################################
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


# require Flask-GoogleMaps (https://github.com/rochacbruno/Flask-GoogleMaps)
# api_key = 'AIzaSyAzeggzDErZuRAL6B4P1eIOxiYZouYLxu8' # change this to your api key

