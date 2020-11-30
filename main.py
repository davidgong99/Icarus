from flask import Flask, jsonify, request, make_response
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

    possibleStates = ["Decomissioned", "Maintenance", "Operational"]

    def __init__(self, name, model, location, state):
        self.id = Spaceship.spaceshipCount
        Spaceship.spaceshipCount += 1
        self.name = name
        self.model = model
        self.location = location
        self.state = state

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # If newState is isn't a valid state, return -1 (and don't mutate current state)
    # Else, update and return 0
    def setState(self, newState):
        if newState not in self.possibleStates:
            return -1
        
        self.state = newState
        return 0
        

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
# =     Helper functions
# =
# ========================

# Checks if all fields exist in the given JSON data
# Arguments:
#   fields: List of strings
#   data: Dictionary with type(key)=string
def checkFields(fields, data):
    for field in fields:
        if field not in data:
            return -1

    return 0

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
    requiredFields = ['name', 'model', 'location', 'state']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    name = data['name']
    model = data['model']
    location = data['location']
    state = data['state']

    # TODO: error if state is invalid

    # Create spaceship
    s = Spaceship(name,model, location, state)

    print(s.toJSON())

    # Add spaceship to collection
    ships[s.id] = s
    return make_response(s.toJSON(), 200)


# ========================
# =
# =      TODO: Update spaceship
# =
# ========================
@app.route('/spaceship', methods = ['PUT'])
def updateShip():

    data = request.json

    # Check that correct fields are supplied
    requiredFields = ['spaceshipID', 'state']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    spaceshipID = data['spaceshipID']
    newState = data['state']

    # Check if spaceship exists
    if spaceshipID not in ships:
        return make_response(jsonify({'response': 'Spaceship does not exist', 'code': 422}), 422)

    # Try update state
    if (ships[spaceshipID].setState(newState) == -1):
        return make_response(jsonify({'response': 'Invalid state', 'code': 422}), 422)

    return ships[spaceshipID].toJSON(), 200

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
    