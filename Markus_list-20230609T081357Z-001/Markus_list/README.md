## Requirements:
run this to install the nessesary modules:
pip install -r requirements.txt

! We used python version 3.10 so that the geopy package would work. !

## To construct the database:
- Create a flask_db database in postgres.
- Remember to update username, password and port info for all connections (app2.py included).
- Run init_db.py

## About the webapp
The purpose of this app is to help people with EV's on Samsø to locate the nearest available charging stations.
To use the app the user must first select socket type of their car, their coordinates and maximum traveling distance.
On the map the user can see all the charging stations on Samsø and their own position. The list button will take the user to a list of the available chargers with the right sockets, sorted in ascending order after distance between charger and user.