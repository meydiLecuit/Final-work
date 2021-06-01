from flask import Flask, Response, request, session, jsonify, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from userCrud import user_api
from productCrud import product_api
from flask_cors import CORS
from connection import db
import json
from werkzeug.utils import secure_filename
import os
#import tensorflow as tf
import errno
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img


auth = HTTPBasicAuth()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)
app.register_blueprint(user_api)
app.register_blueprint(product_api)



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

        print(request)
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
            print(file.filename)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))
                if len(os.listdir(path) ) < 100:
                    data_augmentation(filename)

        flash('File(s) successfully uploaded')

        os.system('py retrain.py --output_graph=retrained_graph.pb --output_labels=retrained_labels.txt --architecture=MobileNet_1.0_224 --image_dir=image_dataset')

        return Response(response=json.dumps({"message":'File successfully uploaded'}), status=200, mimetype="application/json")





@app.route('/login', methods=['GET','POST'])
def login():
  

    user = {"username": request.form["username"],
                "password": request.form["password"]}
    

    userDb = db.users.find_one( {"username": user['username']} )
    
    

    if userDb['username'] == user['username'] and user['password'] == userDb['password']:
        sessionUser = {}
        sessionUser['ID'] = str(userDb['_id'])
        sessionUser['username'] = user['username']
        sessionUser['isLogedIn'] = True
        
        return Response(response=json.dumps(sessionUser), status=200, mimetype="application/json")

    else:
        return Response(response=json.dumps({"message": "Wrong password"}), status=500)
        print("errorerror")




 

if __name__ == "__main__":
    app.run(port=80, debug=True)
