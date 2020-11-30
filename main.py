from flask import Flask, jsonify, request
import json
from json import JSONEncoder

# ========================
# =
# =     JSON Encoder
# =
# ========================
class Encoder(JSONEncoder):
    def default(self, o):
            return o.__dict__

# ========================
# =
# =     Class: Spaceship
# =
# ========================
class Spaceship:
    spaceshipCount = 0

    def __init__(self, name, model, location, status):
        self.id = Spaceship.spaceshipCount
        Spaceship.spaceshipCount += 1
        self.name = name
        self.model = model
        self.location = location
        self.status = status

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# ========================
# =
# =     Class: Location
# =
# ========================
class Location:
    locationCount = 0

    def __init__(self, city, name, planet, capacity):
        self.id = Location.locationCount
        Location.locationCount += 1
        self.city = city
        self.name = name
        self.planet = planet
        self.capacity = capacity

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# ========================
# =
# =     Global variables
# =
# ========================

# Dictionary for keeping track of all spaceships
# key = id, value = Spaceship (object)
ships = {}

# Dictionary for keeping track of all locations
# key = id, value = Location (object)
locations = {}

# Start flaskapp
app = Flask(__name__)

# ========================
# =
# =     Default route
# =
# ========================
@app.route('/')
def hello():
    return 'Welcome to Icarus', 200

# ========================
# =
# =      List spaceships (NOT REQUIRED)
# =
# ========================
@app.route('/spaceship', methods = ['GET'])
def listShips():
    jsonStr = json.dumps(ships, indent=4, cls=Encoder)
    print(jsonStr)
    return jsonStr, 200

# ========================
# =
# =     Add spaceship
# =
# ========================
@app.route('/spaceship', methods = ['POST'])
def addSpaceship():

    data = request.json
   
    # Check that correct fields are supplied
    requiredFields = ['name', 'model', 'location', 'status']
    for field in requiredFields:
        if not field in data:
            abort(400)

    # Extract data
    name = data['name']
    model = data['model']
    location = data['location']
    status = data['status']

    # Create spaceship
    s = Spaceship(name,model, location, status)

    print(s.toJSON())

    # Add spaceship to collection
    ships[s.id] = s
    return s.toJSON(), 200


# ========================
# =
# =      TODO: Update spaceship
# =
# ========================
# TODO: make PUT request
# TODO: add queries
@app.route('/spaceship', methods = ['PUT'])
def updateShip():
    return "/updateShip"

# ========================
# =
# =      TODO: Add location
# =
# ========================
# TODO: make POST request
# TODO: add queries
@app.route('/addLocation')
def addLocation():
    return "/addLocation"

# ========================
# =
# =      TODO: Remove spaceship
# =
# ========================
# TODO: make DEL request
# TODO: add queries
@app.route('/removeShip')
def removeShip():
    return "/removeShip"

# ========================
# =
# =      TODO: Remove location
# =
# ========================
# TODO: make DEL request
# TODO: add queries
@app.route('/removeLocation')
def removeLocation():
    return "/removeLocation"

# ========================
# =
# =      TODO: Travel
# =
# ========================
# TODO: make POST request
# TODO: add queries
@app.route('/travel')
def travel():
    return "/travel"


# ========================
# =
# =     Main
# =
# ========================
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    