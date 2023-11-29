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
        data = {"status" : False, "message" : "Invalid information"}
        return jsonify(data)
    elif (len(email) <= 0 or len(password) <= 0):
        data = {"status" : False, "message" : "Invalid data"}
        return jsonify(data)
    elif (checkUserExistsOrNot(email) is True):
        query = {
        "email": email, "password": password
        }
        collection.insert_one(query)
        data = {"status" : True, "message" : "User created successfully"}
        return jsonify(data)
    else:
        data = {"status" : False, "message" : "User already exists"}
        return jsonify(data)


@app.route("/update", methods=['PUT'])
def updatePassword():

    dbs = client.cleanHires
    collection = dbs.users

    email = request.args.get('email')
    newPassword = request.args.get('password')

    query = {
        "email": email
    }

    value = {"$set" : {
        "password" : newPassword
    }}

    response = collection.update_one(query, value)
    if response.matched_count == 0:
        data = {"status" : False, "message" : "No user found"}
        return jsonify(data)
    else:
        data = {"status" : True, "message" : "Password updated successfully"}
        return jsonify(data)
    

def checkUserExistsOrNot(email):
    dbs = client.cleanHires
    collection = dbs.users

    query = {"email" : email}
    response = collection.count_documents(query)
    if(response == 0):
        return True
    else :
        return False


if __name__ == '__main__':
    app.run(debug=True)
