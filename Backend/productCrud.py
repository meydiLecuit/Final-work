from flask import Flask, Response, request,Blueprint
from connection import db
import json
from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId
import base64
from cv2 import cv2
import label_image





auth = HTTPBasicAuth()
product_api = Blueprint('product_api', __name__)





@product_api.route("/sendPicture", methods=["POST"])
def send_picture():
    if request.method == 'POST':
        json = request.get_json("file")

        
        file = json['file']
        filename = json['name']
        starter = file.find(',')
        image_data = file[starter+1:]
        image_data = bytes(image_data, encoding="ascii")
        with open('image/'+filename, 'wb') as fh:
            fh.write(base64.decodebytes(image_data))
        return 'ok'
    return 'error'

@product_api.route("/prediction", methods=["GET"])
def send_predictionRes():
    try:
        
        def load_image(image):
            text = label_image.main(image)
            img = cv2.imread(image)
            return img,text
        img,text = load_image('./image/case01wd03id01.jpg')
        
        return Response(response=json.dumps(text), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "data not sent"}), status=500, mimetype="application/json")
# Get all products



@product_api.route("/products", methods=["POST"])
def create_product():
    try:
        product = {"name": request.form["name"],
                "prijs": request.form["prijs"], "merk":request.form["merk"]}
        dbResponse = db.products.insert_one(product)

        name = product['name']

        with open("retrained_labels.txt", "r+") as file_object:
            for line in file_object:
                if name in line:
                    break
                else:
                    file_object.write(name)

        data = list(db.produts.find())
        
        for productdb in data:
            
            if(product['name'] == productdb['name']):
                print('Product already exist')
                return Response(response=json.dumps({"message": "product already exist"}), status=409,mimetype="application/json")
            else:
                return Response(response=json.dumps({"message": "product created", "id": f"{dbResponse.inserted_id}"}),status=200, mimetype="application/json")
   
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Product not created"}), status=500, mimetype="application/json")

# Get all products


@product_api.route("/products", methods=["GET"])

def get_products():
    try:
        data = list(db.products.find())
        for product in data:
            product["_id"] = str(product["_id"])

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read products"}), status=500, mimetype="application/json")


@product_api.route("/product/<id>", methods=["GET"])
def get_product(id):
    try:
        
        data = db.products.find_one( {"_id": ObjectId(id)} )
        data["_id"] = str(data["_id"])

        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot find user"}), status=500, mimetype="application/json")

# Update product


@product_api.route("/editProduct/<id>", methods=["PATCH"])
def update_product(id):
    try:
        dbResponse = db.products.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"], "prijs": request.form["prijs"], "merk": request.form["merk"]}
            }
        )
        return Response(response=json.dumps({"message": "product update"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot update users"}), status=500, mimetype="application/json")

# delete product


@product_api.route("/deleteProduct/<id>", methods=["DELETE"])
def delete_product(id):
    try:
        dbResponse = db.products.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"message": "product deleted"}), status=200, mimetype="application/json")
        return Response(response=json.dumps({"message": "product not found"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot delete product"}), status=500, mimetype="application/json")






