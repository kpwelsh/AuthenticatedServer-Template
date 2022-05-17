from flask import Flask, request, jsonify

from flask_cors import CORS

from flask_jwt_extended import create_access_token
#from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import os

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

VALID_USER = os.getenv('VALID_USER')

@app.route('/login', methods = ['POST'])
def login():
    print(request)
    username = request.json.get('username', None)
    if username != VALID_USER:
        return jsonify({'msg': 'Bad user'}), 401
    
    return jsonify(
        access_token = create_access_token(identity=username)
    )


def saveRecord(name, data):
    print('saving some data', name, data)

def deleteRecord(name):
    print('deleting some data', name)

def getRecord(name):
    print('getting some data', name)

@app.route('/record', methods = ['POST', 'GET', 'DELETE'])
@jwt_required()
def record():
    data = request.json
    if request.method == 'POST':
        saveRecord(data['name'], data['frameData'])
    elif request.method == 'GET':
        getRecord(data['name'])
    elif request.method == 'DELETE':
        deleteRecord(data['name'])
    return 200
        
@app.route('/listRecords')
@jwt_required()
def listRecords():
    return jsonify(
        names = ['a', 'b', 'c']
    )

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))