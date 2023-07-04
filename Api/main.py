import json
from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
from paho.mqtt import client as mqtt_client
import random

app = Flask(__name__)

URI = "mongodb://10.100.20.142:27017"
client = None
db = None
col = None

broker = '10.100.20.142'
port = 1883
topic = "temperatur"

temperatur = 0

client_id = f'python-mqtt-{random.randint(0, 1000)}'

@app.route('/cube')
def cube():
    global col
    
    list_cur = col.find()
    json_data = dumps(list_cur)
    
    return json_data, 200, {"Access-Control-Allow-Origin": "*"}

@app.route('/temp')
def temp():
    return { "Temp": temperatur }, 200, {"Access-Control-Allow-Origin": "*"}

def ConnectToDatabase():
    global client
    global db
    global col
    
    client = MongoClient(URI);
    db = client["Roboter"]
    col = db["CubeColor"]
    
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    def on_message(mosq, obj, msg):
        global temperatur
        temperatur = int(msg.payload)
        
    mqttc = mqtt_client.Client(client_id)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(broker, port)
    return mqttc

ConnectToDatabase()
mqttc = connect_mqtt()
mqttc.loop_start()
mqttc.subscribe("temperatur", 0)
app.run()
