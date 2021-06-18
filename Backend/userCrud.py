from flask import Flask, Response, request,Blueprint, current_app
from connection import db
import json
from bson.objectid import ObjectId
import jwt
from functools import wraps


user_api = Blueprint('user_api', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #print(request.headers['Authorization'])
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return Response(response=json.dumps({"message":'Token is missing'}), status=401)
        
        try:
            
            
            data = jwt.decode(token, current_app.config['jwt_key'])
            print(data)
            current_user = db.users.find_one( {"_id": data['_id']} )
        except:
            return Response(response=json.dumps({"message":'Token is invalid'}), status=401)

        return f(current_user, *args, **kwargs)

    return decorated





@user_api.route("/getUser/<id>", methods=["GET"])
@token_required
def get_user(current_user,id):
    try:
        
        data = db.users.find_one( {"_id": ObjectId(id)} )
        data["_id"] = str(data["_id"])
        data["password"] = str(data["password"])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot find user"}), status=500, mimetype="application/json")


# Get all users

@user_api.route("/getUsers", methods=["GET"])
@token_required
def get_users(current_user):
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
            user["password"] = str(user["password"])

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}), status=500, mimetype="application/json")

# Update user
@user_api.route("/editUser/<id>", methods=["PATCH"])
@token_required
def update_user(current_user,id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
           {"$set": {"name": request.form["name"], "lastName": request.form["lastName"], "username": request.form["username"], "email": request.form["email"] }
           }

        )
        return Response(response=json.dumps({"message": "user update"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot update users"}), status=500, mimetype="application/json")

# delete user
@user_api.route("/deleteUser/<id>", methods=["DELETE"])
@token_required
def delete_user(current_user,id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"message": "user deleted"}), status=200, mimetype="application/json")
        return Response(response=json.dumps({"message": "user not found"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot delete user"}), status=500, mimetype="application/json")