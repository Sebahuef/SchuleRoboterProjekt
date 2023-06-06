import DoBotArm as Dbt
from paho.mqtt import client as mqtt_client
import random
import json

Color = None

broker = '10.100.20.142'
port = 1883
topic = "CubeColor"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
    
def main():
    client = connect_mqtt()
    client.loop_start()
    
    print(Color)
    
    homeX, homeY, homeZ = 257, 4, 76, 
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    
    while True:
        
        if Color != None:
        
            input("Start:")
        
            ctrlBot.toggleSuction()
            ctrlBot.moveArmXYZ(286,12,-36)
    
            ctrlBot.moveHome()
    
            if Color == "Red":
                ctrlBot.moveArmXYZ(182,190,-29)
            elif Color == "Blue":
                ctrlBot.moveArmXYZ(113,242,-32)
            elif Color == "Green":
                ctrlBot.moveArmXYZ(39,275,-33)
            else:
                print("No Color detected")
        
            ctrlBot.toggleSuction()
            ctrlBot.moveHome()
            
        else:
            print("Color None")
        
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            
            client.subscribe("CubeColor")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    def on_message(client, userdata, msg):
        global Color
        
        Data = json.loads(msg.payload)
        Color = Data['color']
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client

main()


