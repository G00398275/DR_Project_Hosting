'''Data Representation - Winter 2022
Big Project: rest_server.py
Author: Ross Downey (G00398275)
Lecturer: Andrew Beatty'''

from flask import Flask,url_for, request, abort, jsonify # import necessary functions from flask

from nflDAO2 import nflDAO

app = Flask(__name__, static_url_path='', static_folder='static_pages')

# array of quarterbacks
quarterbacks=[
    {"id": 1, "Name": "Patrick Mahomes", "Team": "Kansas City Chiefs", "Yards": 3585, "TDs": 29, "INTs": 8},
    {"id": 2, "Name": "Josh Allen", "Team": "Buffalo Bills", "Yards": 3183, "TDs": 23, "INTs": 11},
    {"id": 3, "Name": "Joe Burrow", "Team": "Cincinnati Bengals", "Yards": 3160, "TDs": 23, "INTs": 8}
]

# array of runningbacks
runningbacks=[
    {"id": 1, "Name": "Josh Jacobs", "Team": "Las Vegas Raiders", "Yards": 1159, "ATTs": 216, "TDs": 9},
    {"id": 2, "Name": "Derrick Henry", "Team": "Tennessee Titans", "Yards": 1048, "ATTs": 247, "TDs": 10},
    {"id": 3, "Name": "Nick Chubb", "Team": "Cleveland Browns", "Yards": 1039, "ATTs": 200, "TDs": 12}
]
# global variable needed for create function
nextId = 4

# Test getAll function using: curl http://127.0.0.1:5000//nflstats/quarterbacks
@app.route('/nflstats/quarterbacks')
def getAllQBs():
    results = nflDAO.getAllQBs()
    return jsonify(results)

# Test findById function using: curl http://127.0.0.1:5000/nflstats/quarterbacks/1 for example
@app.route('/nflstats/quarterbacks/<int:id>')
def findById(id):
    #foundQBs = list(filter(lambda t : t["id"] == id, quarterbacks)) # lambda function
    foundQBs = nflDAO.findQBByID(id)
    if len(foundQBs) == 0:
        return jsonify({}), 204 # 204 code, no content
    return jsonify(foundQBs)


# Test create function using curl -X POST -H "content-type:application/json" -d "{\"Name\": \"Tom Brady\",\"Team\": \"Tampa Bay Buccaneers\", \"Yards\": 3000, \"TDs\": 14, \"INTs\": 2}" http://127.0.0.1:5000/nflstats/quarterbacks
@app.route('/nflstats/quarterbacks', methods=['POST'])
def create():
    if not request.json:
        abort(400) # 400 code, bad request if not in json format
    QB = {
        "Name": request.json["Name"],
        "Team": request.json["Team"],
        "Yards": request.json["Yards"], 
        "TDs": request.json["TDs"],
        "INTs": request.json["INTs"]
    }
    # Tuple Conversion Required
    values = (QB['Name'], QB['Team'], QB['Yards'],
            QB['TDs'], QB['INTs'])
 
    newId = nflDAO.createQBs(values)
    QB['id'] = newId
    return jsonify(QB)


# Test update function using: curl -X PUT -d "{\"Name\":\"Patrick Allen\",\"Team\": \"Kansas City Bills\", \"Yards\": 10000, \"TDs\": 10000, \"INTs\": 10000}" -H "content-type:application/json" http://127.0.0.1:5000/nflstats/quarterbacks/1
@app.route('/nflstats/quarterbacks/<int:id>', methods=['PUT'])
def update(id):
    #foundQBs = list(filter(lambda t: t["id"] == id,quarterbacks))
    foundQB = nflDAO.findQBByID(id)
    
    if not foundQB:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Yards' in reqJson and type(reqJson['Yards']) is not int:
        abort(400)
    if 'TDs' in reqJson and type(reqJson['TDs']) is not int:
        abort(400)
    if 'INTs' in reqJson and type(reqJson['INTs']) is not int:
        abort(400)
    #currentQB = foundQB[0]
    if 'Name' in reqJson:
        foundQB['Name'] = reqJson['Name']
    if 'Team' in reqJson:
        foundQB['Team'] = reqJson['Team']
    if 'Yards' in reqJson:
        foundQB['Yards'] = reqJson['Yards'] 
    if 'TDs' in reqJson:
        foundQB['TDs'] = reqJson['TDs']
    if 'INTs' in reqJson:
        foundQB['INTs'] = reqJson['INTs']
    
    # Tuple Conversion Required, INT object does not support item assignment error received.
    values = (foundQB['Name'],foundQB['Team'],foundQB['Yards'],foundQB['TDs'],foundQB['INTs'],foundQB['id'])

    nflDAO.updateQBs(values)
    return jsonify(foundQB)

# Test delete function using: curl -X DELETE http://127.0.0.1:5000/nflstats/quarterbacks/1
@app.route('/nflstats/quarterbacks/<int:id>', methods=['DELETE'])
def delete(id):
    #foundQBs = list(filter(lambda t: t["id"] == id, quarterbacks))
    foundQBs = nflDAO.findQBByID(id)
    if len(foundQBs) == 0:
        return jsonify({}), 404 
    #quarterbacks.remove(foundQBs[0])
    nflDAO.deleteQB(id)

    return jsonify({"done": True})

'''------------------------RUNNING BACKS-------------------------------------------------'''

# Test getAll function using: curl http://127.0.0.1:5000//nflstats/runningbacks
@app.route('/nflstats/runningbacks')
def getAllRBs():
    results = nflDAO.getAllRBs()
    return jsonify(results)

# Test findById function using: curl http://127.0.0.1:5000/nflstats/runningbacks/1 for example
@app.route('/nflstats/runningbacks/<int:id>')
def findRBById(id):
    #foundRBs = list(filter(lambda t : t["id"] == id, runningbacks)) # lambda function
    foundRBs = nflDAO.findRBByID(id)
    if len(foundRBs) == 0:
        return jsonify({}), 204 # 204 code, no content
    return jsonify(foundRBs)


# Test create function using curl -X POST -H "content-type:application/json" -d "{\"Name\": \"Tom Brady\",\"Team\": \"Tampa Bay Buccaneers\", \"Yards\": 3000, \"ATTs\": 14, \"TDs\": 2}" http://127.0.0.1:5000/nflstats/runningbacks
@app.route('/nflstats/runningbacks', methods=['POST'])
def createRB():
    if not request.json:
        abort(400) # 400 code, bad request if not in json format
    RB = {
        "Name": request.json["Name"],
        "Team": request.json["Team"],
        "Yards": request.json["Yards"], 
        "ATTs": request.json["ATTs"],
        "TDs": request.json["TDs"]
    }
    # Tuple Conversion Required
    values = (RB['Name'], RB['Team'], RB['Yards'],
            RB['ATTs'], RB['TDs'])
 
    newRBId = nflDAO.createRBs(values)
    RB['id'] = newRBId
    return jsonify(RB)


# Test update function using: curl -X PUT -d "{\"Name\":\"Patrick Allen\",\"Team\": \"Kansas City Bills\", \"Yards\": 10000, \"ATTs\": 10000, \"TDs\": 10000}" -H "content-type:application/json" http://127.0.0.1:5000/nflstats/runningbacks/1
@app.route('/nflstats/runningbacks/<int:id>', methods=['PUT'])
def updateRB(id):
    #foundQBs = list(filter(lambda t: t["id"] == id,quarterbacks))
    foundRB = nflDAO.findRBByID(id)
    
    if not foundRB:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Yards' in reqJson and type(reqJson['Yards']) is not int:
        abort(400)
    if 'ATTs' in reqJson and type(reqJson['ATTs']) is not int:
        abort(400)
    if 'TDs' in reqJson and type(reqJson['TDs']) is not int:
        abort(400)
    
    if 'Name' in reqJson:
        foundRB['Name'] = reqJson['Name']
    if 'Team' in reqJson:
        foundRB['Team'] = reqJson['Team']
    if 'Yards' in reqJson:
        foundRB['Yards'] = reqJson['Yards'] 
    if 'TDs' in reqJson:
        foundRB['ATTs'] = reqJson['ATTs']
    if 'INTs' in reqJson:
        foundRB['TDs'] = reqJson['TDs']
    
    # Tuple Conversion Required, INT object does not support item assignment error received.
    valuesRB = (foundRB['Name'],foundRB['Team'],foundRB['Yards'],foundRB['ATTs'],foundRB['TDs'],foundRB['id'])

    nflDAO.updateRBs(valuesRB)
    return jsonify(foundRB)

# Test delete function using: curl -X DELETE http://127.0.0.1:5000/nflstats/runningbacks/1
@app.route('/nflstats/runningbacks/<int:id>', methods=['DELETE'])
def deleteRB(id):
    #foundRBs = list(filter(lambda t: t["id"] == id, runningbacks))
    foundRBs = nflDAO.findRBByID(id)
    if len(foundRBs) == 0:
        return jsonify({}), 404 
    #quarterbacks.remove(foundQBs[0])
    nflDAO.deleteRB(id)

    return jsonify({"done": True})

if __name__ == "__main__":
    app.run(debug = True) 