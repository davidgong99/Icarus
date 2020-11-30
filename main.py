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
        if state not in self.possibleStates:
            raise ValueError("Invalid state")

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


    # TODO: check if inputted location exists

    # Create spaceship
    try:
        s = Spaceship(name,model, location, state)
    except ValueError:
        return make_response(jsonify({'response': 'Invalid state', 'code': 422}), 422)

    print(s.toJSON())

    # Add spaceship to collection
    ships[s.id] = s
    return make_response(s.toJSON(), 200)


# ========================
# =
# =      Update spaceship
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
# =      List locations (NOT REQUIRED)
# =
# ========================
@app.route('/location', methods = ['GET'])
def listLocations():
    jsonStr = json.dumps(locations, indent=4, cls=Encoder)
    print(jsonStr)
    return jsonStr, 200

# ========================
# =
# =      TODO: Add location
# =
# ========================
# TODO: make POST request
# TODO: add queries
@app.route('/location', methods = ['POST'])
def addLocation():

    data = request.json

    # Check that correct fields are supplied
    requiredFields = ['city', 'name', 'planetName', 'capacity']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    city = data['city']
    name = data['name']
    planetName = data['planetName']
    capacity = data['capacity']

    # Create location
    try:
        loc = Location(city, name, planetName, capacity)
    except ValueError:
        return make_response(jsonify({'response': 'Invalid state', 'code': 422}), 422)

    locations[loc.id] = loc

    return loc.toJSON(), 200

# ========================
# =
# =      Remove spaceship
# =
# ========================
@app.route('/spaceship', methods = ['DELETE'])
def removeShip():

    data = request.json

    # Check that correct fields are supplied
    requiredFields = ['spaceshipID']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    id = data['spaceshipID']

    # Check the ship exists
    if id not in ships:
        return make_response(jsonify({'response': 'Spaceship could not be found', 'code': 404}), 404)

    # Delete ship
    del ships[id]

    return make_response(jsonify({'response': 'OK', 'code': 200}), 200)

# ========================
# =
# =      Remove location
# =
# ========================
@app.route('/location', methods = ['DELETE'])
def removeLocation():

    data = request.json

    # Check that correct fields are supplied
    requiredFields = ['locationID']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    id = data['locationID']

    # Check the ship exists
    if id not in locations:
        return make_response(jsonify({'response': 'Location could not be found', 'code': 404}), 404)

    # Delete ship
    del locations[id]

    return make_response(jsonify({'response': 'OK', 'code': 200}), 200)

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
    