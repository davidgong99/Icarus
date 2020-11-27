from flask import Flask, jsonify



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
        jDict = {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'location': self.location,
            'status': self.status
        }
        return jDict

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to Icarus'

@app.route('/addSpaceship')
def addSpaceship():
    s = Spaceship('Name','MyModel','Thislocation','Maintenance')
    print(s.toJSON())

    return s.toJSON()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    