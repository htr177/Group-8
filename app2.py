from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__, template_folder="templates") 
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCtzTSyDxwFhEfsyJazopYkbXmIehHXVTM"
GoogleMaps(app)


@app.route('/')
def mapview():
    mymap = Map(
        identifier="view-side",
        lat=55.827037,
        lng=10.596938,
        zoom=10,
        style="height:500px;width:1000px;margin:0;",
        markers=[(55.831128, 10.593543), (55.827037, 10.596938)]
    ) 
    return render_template('map.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)    