# Icarus
Basic REST API for tracking objects

## Specs
Python version 3.8.5

To install all required packages: `pip3 install -r requirements.txt`

To run: `py main.py`

## Task


## Requirements


## Routes and responses

**List all spaceships**

`GET`

http://localhost:5000/spaceship

Returns all spaceships that exist (ordered by ID) in JSON form

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
---

**Add spaceship**

`POST`

http://localhost:5000/spaceship

Creates a spaceship with the given information

Example payload:
```python
{
    "name": "Shippy",
    "model": "Fast",
    "location": 1,
    "state": "Maintenance"
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Location does not exist         |
| 422  | Invalid state                   |

---

**Update a spaceship's state**

`PUT`

http://localhost:5000/spaceship

Update a spaceship's state to another state.

Possible states:
* Decommissioned
* Maintenance
* Operational

`spaceshipID` must match an existing spaceship

`state` must match one of the possible states

Example payload:
```python
{
    "spaceshipID": 1,
    "state": "Operational"
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Spaceship does not exist        |
| 422  | Invalid state                   |

---

**Add location**

`POST`

http://localhost:5000/location

Creates a location with the given information

Example payload:
```python
{
    "city": "Sydney",
    "name": "Gas station",
    "planetName": "Earth",
    "capacity": 50
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Invalid capacity                |


---

**Remove a spaceship**

`DEL`

http://localhost:5000/spaceship

Removes a spaceship with a matching ID

Example payload:
```python
{
    "spaceshipID": 1
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Spaceship could not be found    |

---

**Remove a location**

`DEL`

http://localhost:5000/location

Removes a location with a matching ID

Example payload:
```python
{
    "locationID": 1
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Location could not be found     |

---

**Travel**

`POST`

http://localhost:5000/travel


Example payload:
```python
{
    "spaceshipID": 0,
    "locationID": 1,
}
```

| Code |        Reason/Response          |
|------| --------------------------------|
| 200  | OK                              |
| 400  | Bad request                     |
| 422  | Spaceship does not exist        |
| 422  | Location does not exist         |
| 422  | Spaceship is not operational    |
| 422  | Location is at maximum capacity |

