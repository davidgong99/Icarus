from flask import Flask, jsonify, request, make_response, render_template
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
        # check if state is valid
        if state not in self.possibleStates:
            raise ValueError("Invalid state")

        # check if location is already full - if not, add ship to it
        if locations[location].atMaxCapacity():
            raise ValueError("Location is at maximum capacity")
        else:
            locations[location].capacity += 1

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
        
    # If spaceship is operational, then it can travel - return 1
    # Else, return 0
    def canTravel(self):
        if self.state == "Operational":
            return 1
        return 0

    def travel(self, newLocation):
        # Check if spaceship is operational
        if not self.canTravel():
            raise ValueError('Spaceship is not operational')
            # return make_response(jsonify({'response': 'Spaceship is not operational', 'code': 422}), 422)

        # Check if inputted location has enough capacity
        if locations[newLocation].atMaxCapacity():
            raise ValueError('Location is at maximum capacity')
            # return make_response(jsonify({'response': 'Location is at maximum capacity', 'code': 422}), 422)

        
        # Decrease current location's capacity
        locations[self.location].capacity -= 1

        # Increase new location's capacity
        locations[newLocation].capacity += 1

        # Move ship to new location
        self.location = newLocation

        return 0


# ========================
# =
# =     Class: Location
# =
# ========================
class Location:
    locationCount = 0

    def __init__(self, city, name, planet, maxCapacity):
        if maxCapacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        
        self.id = Location.locationCount
        Location.locationCount += 1
        self.city = city
        self.name = name
        self.planet = planet
        self.maxCapacity = maxCapacity # maximum threshold
        self.capacity = 0 # tracking ships currently at location

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # If location is at maximum capacity, return 1
    # Else return 0
    def atMaxCapacity(self):
        if self.capacity < self.maxCapacity:
            return 0
        return 1

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
    return render_template('forms.html')
    return 'Welcome to Icarus', 200

# ========================
# =
# =      List spaceships (NOT REQUIRED)
# =
# ========================
@app.route('/spaceship', methods = ['GET'])
def listShips():
    res = {}
    for s in ships.values():
        res[s.id] = s.toJSON()
    return res

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

    try:
        location = int(data['location'])
    except Exception as e:
        return make_response(jsonify({'response': 'Location does not exist', 'code': 422}), 422)

    state = data['state']

    # location = int(location)

    # Check if inputted location exists
    if location not in locations:
        return make_response(jsonify({'response': 'Location does not exist', 'code': 422}), 422)

    # Create spaceship
    try:
        s = Spaceship(name,model, location, state)
    except ValueError as e:
        return make_response(jsonify({'response': str(e), 'code': 422}), 422)

    # Add spaceship to collection
    ships[s.id] = s

    return s.toJSON(), 200


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
    newState = data['state']

    try:
        spaceshipID = int(data['spaceshipID'])
    except Exception as e:
        return make_response(jsonify({'response': 'Spaceship does not exist', 'code': 422}), 422)


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
    res = {}
    for l in locations.values():
        res[l.id] = l.toJSON()
    return res


# ========================
# =
# =      Add location
# =
# ========================
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

    try:
        capacity = int(data['capacity'])
    except Exception as e:
        return make_response(jsonify({'response': "Capacity must be a positive integer", 'code': 422}), 422)


    # Create location
    try:
        loc = Location(city, name, planetName, capacity)
    except ValueError as e:
        return make_response(jsonify({'response': str(e), 'code': 422}), 422)

    # Add location to collection
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
    try:
        id = int(data['spaceshipID'])
    except Exception as e:
        return make_response(jsonify({'response': 'Spaceship could not be found', 'code': 422}), 422)


    # Check the ship exists
    if id not in ships:
        return make_response(jsonify({'response': 'Spaceship could not be found', 'code': 422}), 422)

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
    try:
        id = int(data['locationID'])
    except Exception as e:
        return make_response(jsonify({'response': 'Location could not be found', 'code': 422}), 422)

    # Check the ship exists
    if id not in locations:
        return make_response(jsonify({'response': 'Location could not be found', 'code': 422}), 422)

    # Delete ship
    del locations[id]

    return make_response(jsonify({'response': 'OK', 'code': 200}), 200)

# ========================
# =
# =      Travel
# =
# ========================
@app.route('/travel', methods = ['POST'])
def travel():

    data = request.json

    # Check that correct fields are supplied
    requiredFields = ['spaceshipID', 'locationID']
    if (checkFields(requiredFields, data) == -1):
        return make_response(jsonify({'response': 'Bad request', 'code': 400}), 400)

    # Extract data
    try:
        spaceshipID = int(data['spaceshipID'])
    except Exception as e:
        return make_response(jsonify({'response': 'Spaceship does not exist', 'code': 422}), 422)

    try:
        locationID = data['locationID']
    except Exception as e:
        return make_response(jsonify({'response': 'Location does not exist', 'code': 422}), 422)

    # Check if inputted spaceship exists
    if spaceshipID not in ships:
        return make_response(jsonify({'response': 'Spaceship does not exist', 'code': 422}), 422)

    # Check if inputted location exists
    if locationID not in locations:
        return make_response(jsonify({'response': 'Location does not exist', 'code': 422}), 422)

    # Move ship to location
    try:
        ships[spaceshipID].travel(locationID)
    except ValueError as e:
        return make_response(jsonify({'response': str(e), 'code': 422}), 422)

    return make_response(jsonify({'response': 'OK', 'code': 200}), 200)


# ========================
# =
# =     Main
# =
# ========================
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    