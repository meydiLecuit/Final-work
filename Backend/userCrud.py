from flask import Flask, Response, request,Blueprint
from connection import db
import json
from bson.objectid import ObjectId


user_api = Blueprint('user_api', __name__)

#@user_api.route("/register", methods=['post', 'get'])
#def index():
 #   message = ''
  #  if "email" in session:
   #     return redirect(url_for("index"))
   # if request.method == "POST":
    #    firstname= request.form.get('firstname')
     #   lastname= request.form.get('lastname')

      #  username = firstname + lastName
      #  email = request.form.get("email")
        
       # password1 = request.form.get("password1")
       # password2 = request.form.get("password2")
        
       # user_found = users.find_one({"username": user})
        #email_found = users.find_one({"email": email})
       # if user_found:
       #     message = 'There already is a user by that name'
       #     return render_template('Frontend/addUser.html', message=message)
       # if email_found:
        #    message = 'This email already exists in database'
        #    return render_template('Frontend/addUser.html', message=message)
       # if password1 != password2:
        #    message = 'Passwords should match!'
        #    return render_template('Frontend/addUser.html', message=message)
       # else:
        #    hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        #    user_input = {'username': username, 'email': email, 'password': hashed}
         #   users.insert_one(user_input)
            
         #   user_data = users.find_one({"email": email})
         #   new_email = user_data['email']
   
         #   return render_template('Frontend/index.html', email=new_email)
    # return render_template('Frontend/addUser.html')



@user_api.route("/getUser/<id>", methods=["GET"])
def get_user(id):
    try:
        
        data = db.users.find_one( {"_id": ObjectId(id)} )
        data["_id"] = str(data["_id"])

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot find user"}), status=500, mimetype="application/json")

@user_api.route("/createUser", methods=["POST"])
def create_user():
    try:
        user = {"name": request.form["name"],
                "lastName": request.form["lastName"],
                "username": request.form["username"],
                "email": request.form["email"],
                "password": request.form["password"],
                "admin": request.form["admin"]
                }
        dbResponse = db.users.insert_one(user)

        return Response(
            response=json.dumps(
                {"message": "user created",
                 "id": f"{dbResponse.inserted_id}"
                 }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
# Get all users

@user_api.route("/getUsers", methods=["GET"])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}), status=500, mimetype="application/json")

# Update user
@user_api.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )
        return Response(response=json.dumps({"message": "user update"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot update users"}), status=500, mimetype="application/json")

# delete user
@user_api.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"message": "user deleted"}), status=200, mimetype="application/json")
        return Response(response=json.dumps({"message": "user not found"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot delete user"}), status=500, mimetype="application/json")