from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankApi
users = db['Users']

def userExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True
    

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']

        if userExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Own": 0,
            "Debt": 0
        })

        retJson = {
            "status": 200,
            "msg": "You have successfully signed up for API"
        }
        return jsonify(retJson)
    
def verifyPw(username, password):
    if not userExist(username):
        return False
    
    hashed_pw = users.find({
        "Username": username
    })[0]['Password']

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
    

def checkWithUser(username):
    cash = users.find({
        "Username": username
    })[0]["Own"]
    return cash

def checkWithUser(username):
    debt = users.find({
        "Username": username
    })[0]["Debt"]
    return debt