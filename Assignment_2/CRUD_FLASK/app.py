from flask import Flask
from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'secretkey'

app.config['MONGO_URI'] = "mongodb://localhost:27017/local"

mongo = PyMongo(app)


@app.route('/add', methods=['Post'])
def add_user():
    _json = request.json
    _name = _json['name']
    _client = _json['client-no']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == "POST":

        _hashed_password = generate_password_hash(_password)

    # if mongo.db.user.find_one({'_client': "client-no"})

        id = mongo.db.user.insert(
            {'name': _name,
             'email': _email,
             'pwd': _hashed_password
                                   })
        resp = jsonify("user added Successfully")
        resp.status_code = 200

        return resp
    else:
        return not_found()

@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete(id):
    mongo.db.user.delete_one({"_id": ObjectId(id)})
    resp = jsonify({
        "Status": 'user deleted sucessfully'
    })
    return resp

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)

        mongo.db.user.update_one({'_id': ObjectId(_id["$oid"]) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})

        resp = jsonify("user updated successfully")

        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)


