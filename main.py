from flask import Flask, jsonify
# from json import JSONEncoder, json
import json
from json import JSONEncoder

class SpaceshipEncoder(JSONEncoder):
    def default(self, o):
            return o.__dict__

# class Encoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__


# key = id, value = Spaceship (object)
ships = {}

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

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to Icarus'

@app.route('/addShip')
def addSpaceship():
    s = Spaceship('Name','MyModel','Thislocation','Maintenance')
    print(s.toJSON())

    ships[s.id] = s

    return s.toJSON()

@app.route('/listShips')
def listShips():
    jsonStr = json.dumps(ships, indent=4, cls=SpaceshipEncoder)
    print(jsonStr)
    return jsonStr

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    