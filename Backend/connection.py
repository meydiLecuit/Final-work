import pymongo


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.FinalWork
    mongo.server_info()

except:
    print("ERROR Cannot connect to db")
