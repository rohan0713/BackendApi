from flask import Flask, jsonify, request, url_for
from mongoConnection import client

app = Flask(__name__)

@app.route('/')
def apiStatus():
    result = "Hi! Welcome to Clean hires backend! Use the data carefully"
    return jsonify(result)

@app.route('/authenticate', methods=['GET'])
def authenticateUser():
    
    dbs = client.cleanHires
    collection = dbs.users

    email = request.args.get('email')
    password = request.args.get('password')
    print(email + " " + password)
    query = {"email": email, "password": password}

    result = collection.find_one(query)
    if result is None:
        data = {"status" : False, "message": "user not found"}
        return jsonify(data)
    else :
        data = {"status" : True, "message": "user found"}
        return jsonify(data)

@app.route("/create", methods=['POST'])
def createUser():
    
    dbs = client.cleanHires
    collection = dbs.users

    email = request.args.get('email')
    password = request.args.get('password')
    print(email)
    print(password)
    
    if(email is None or password is None):
        return jsonify('Add valid query params in url')
    elif (len(email) <= 0 or len(password) <= 0):
        return jsonify('Invalid data')

    query = {
        "email": email, "password": password
    }

    collection.insert_one(query)
    data = {"status" : True}
    return jsonify(data)

@app.route("/update", methods=['PUT'])
def updatePassword():

    dbs = client.cleanHires
    collection = dbs.users

    email = request.args.get('email')
    password = request.args.get('password')

    newPassword = request.args.get('new')

    query = {
        "email": email, "password": password
    }

    value = {"$set" : {
        "password" : newPassword
    }}

    response = collection.update_one(query, value)
    if response.matched_count == 0:
        return 'No data found', 404
    else:
        return 'Email updated successfully'

if __name__ == '__main__':
    app.run(debug=True)