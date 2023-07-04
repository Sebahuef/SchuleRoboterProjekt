import DoBotArm as Dbt
import random
import json
import socket
import asyncio
import pymongo
from paho.mqtt import client as mqtt_client

broker = '10.100.20.142'
port = 1883
topic = "temperatur"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

myclient = None
myDb = None
myCol = None

def main():
    homeX, homeY, homeZ = 257, 4, 76, 
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    
    while True:
        
        global mycol
        
        input("Start:")
            
        Color = GetCurrentColor()
        
        ctrlBot.toggleSuction()
        ctrlBot.moveArmXYZ(286,12,-36)
    
        ctrlBot.moveHome()
    
        if Color == "red":
            ctrlBot.moveArmXYZ(182,190,50)
            ctrlBot.moveArmXYZ(182,190,-33)
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(182,190,50)
        elif Color == "blue":
            ctrlBot.moveArmXYZ(113,242,50)
            ctrlBot.moveArmXYZ(113,242,-33)
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(113,242,50)
        elif Color == "green":
            ctrlBot.moveArmXYZ(39,275,50)
            ctrlBot.moveArmXYZ(39,275,-33)
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(39,275,50)
        else:
            print("No Color detected")
        
        ctrlBot.moveHome()
        
        mydict = { "Color": Color, "Status": "1", "Type": "Cube" }
        mycol.insert_one(mydict)
        
        mqttc.publish("temperatur", str(GetCurrentTemp()))
            
def get_colour_name(b_mean, g_mean, r_mean):
    currentColor = ""
    if (b_mean > g_mean and b_mean > r_mean) :
        currentColor = "blue"
    elif (g_mean > r_mean and g_mean > b_mean) :
        currentColor = "green"
    else:
        currentColor = "red"
    return currentColor

def GetCurrentColor():
    HOST = "10.62.255.10"
    PORT = 4840
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                data = "get color"
                s.sendall(bytes(data, "ascii"))
                data = s.recv(1024)
                actual_name = get_colour_name(data[0], data[1], data[2])
                s.sendall(bytes("close", "ascii"))
                s.close()
                
                return actual_name
            except KeyboardInterrupt:
                s.sendall(bytes("close", "ascii"))
                s.close()
                
def GetCurrentTemp():
    HOST = "10.62.255.10"
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                data = "get temp"
                s.sendall(bytes(data, "ascii"))
                data = s.recv(1024)
                s.sendall(bytes("close", "ascii"))
                s.close()
                
                temp = int.from_bytes(data, byteorder='big')
                
                return temp
            except KeyboardInterrupt:
                s.sendall(bytes("close", "ascii"))
                s.close()
                
async def ConnectToDatabase():
    global myclient
    global mydb
    global mycol
    
    myclient = pymongo.MongoClient("mongodb://10.100.20.142:27017/")
    
    mydb = myclient["Roboter"]
    mycol = mydb["CubeColor"]
    print("Connected to MongoDB")
    
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    mqttc = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    mqttc.on_connect = on_connect
    mqttc.connect(broker, port)
    return mqttc

asyncio.run(ConnectToDatabase())
mqttc = connect_mqtt()
mqttc.loop_start()
main()
