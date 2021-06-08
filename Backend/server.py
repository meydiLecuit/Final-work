from flask import Flask, Response, request, session, jsonify, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from userCrud import user_api
from productCrud import product_api
from flask_cors import CORS
from connection import db
from flask_bcrypt import Bcrypt
import json
from werkzeug.utils import secure_filename
import os
import errno
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)
bcrypt = Bcrypt(app)
app.register_blueprint(user_api)
app.register_blueprint(product_api)
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = none

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         if not token:
#             return Response(response=json.dumps({"message":'Token is missing'}), status=401)
        
#         try:
#             data = jwt.decode(token, app.secret_key)
#             current_user = db.users.find_one( {"_id": data['_id']} )
#         except:
#             return Response(response=json.dumps({"message":'Token is invalid'}), status=401)

#         return f(current_user, *args, **kwargs)

#     return decorated




path = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(path,'image_dataset')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/savePicture', methods=['POST'])
def upload_file():
    if request.method == 'POST':

       
        if 'files[]' not in request.files:
            flash('No file part')
            return Response(response=json.dumps({"message":'No file part'}), status=500, mimetype="application/json")

        
        files = request.files.getlist('files[]')
        className= request.form['name']
        
        path = app.config['UPLOAD_FOLDER']+ "/" + className

        try:
            os.mkdir(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


        def data_augmentation(filename):
            datagen = ImageDataGenerator(
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')

            img = load_img(path +'/' + filename )  # this is a PIL image
            x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
            x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

                # the .flow() command below generates batches of randomly transformed images
                # and saves the results to the `preview/` directory
            i = 0
            for batch in datagen.flow(x, batch_size=1,
                                        save_to_dir='image_dataset/'+className, save_prefix=className, save_format='jpeg'):
                i += 1
                if i > 49:
                    break      
                
        for file in files:
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))
                if len(os.listdir(path) ) < 100:
                    data_augmentation(filename)

        flash('File(s) successfully uploaded')

        os.system('py retrain.py --output_graph=retrained_graph.pb --output_labels=retrained_labels.txt --architecture=MobileNet_1.0_224 --image_dir=image_dataset')

        return Response(response=json.dumps({"message":'File successfully uploaded'}), status=200, mimetype="application/json")


@app.route("/createUser", methods=["POST"])
def create_user():
    try:
        password = request.form["password"]
        pw_hash = bcrypt.generate_password_hash(password)
        
        User = {"name": request.form["name"],
                "lastName": request.form["lastName"],
                "username": request.form["username"],
                "email": request.form["email"],
                "password": pw_hash,
                "admin": request.form["admin"]
                }
        
        data = list(db.users.find())
           
        
        for userdb in data:
            
            if(User['email'] == userdb['email']):
                print('User already exist')
                return Response(response=json.dumps({"message": "user already exist"}), status=409,mimetype="application/json")
            else:
                print('Good')
                dbResponse = db.users.insert_one(User)
                return Response(response=json.dumps({"message": "user created"}),status=200,mimetype="application/json")

       
              
        
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "User not created"}), status=500, mimetype="application/json")



@app.route('/login', methods=['GET','POST'])
def login():
  

    user = {"email": request.form["email"],
                "password": request.form["password"]}
    

    userDb = db.users.find_one( {"email": user['email']} )
    #userDb['password'] == user['username']
    passwordDb =userDb['password']
    #bcrypt.check_password_hash(passwordDb, user['password'])
    if userDb['email'] == user['email'] and bcrypt.check_password_hash(passwordDb, user['password'])   :
     #   token = jwt.encode({'_id': userDb['_id'], 'exp': datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)})
        sessionUser = {}
        sessionUser['ID'] = str(userDb['_id'])
        sessionUser['email'] = user['email']
        sessionUser['isLogedIn'] = True
        
        return Response(response=json.dumps(sessionUser ), status=200, mimetype="application/json")

    else:
        return Response(response=json.dumps({"message": "Wrong password"}), status=500)
        print("errorerror")




 

if __name__ == "__main__":
    app.run(port=80, debug=True)
