from flask import Flask, jsonify
from mongoConnection import client

app = Flask(__name__)

@app.route('/')
def apiStatus():
    result = "Hi! Welcome to Clean hires backend! Use the data carefully"
    return jsonify(result)

@app.route('/authenticate/<string:email>/<string:password>', methods=['GET'])
def authenticateUser(email, password):
    
    dbs = client.cleanHires
    collection = dbs.users
    query = {"email": email, "password": password}

    result = collection.find_one(query)
    if result is None:
        return jsonify("No users found")
    else :
        return jsonify("user found")

if __name__ == '__main__':
    app.run(debug=True)
