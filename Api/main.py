import json
from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

URI = "mongodb://10.100.20.142:27017"
client = None
db = None
col = None


@app.route('/cube')
def index():
    global col
    
    list_cur = col.find()
    json_data = dumps(list_cur)
    
    return json_data, 200, {"Access-Control-Allow-Origin": "*"}

def ConnectToDatabase():
    global client
    global db
    global col
    
    client = MongoClient(URI);
    db = client["Roboter"]
    col = db["CubeColor"]

ConnectToDatabase()
app.run()