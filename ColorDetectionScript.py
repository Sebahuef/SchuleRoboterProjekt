from paho.mqtt import client as mqtt_client
import random
import numpy as np
import cv2
import json

print("Loading Camera...")
vid = cv2.VideoCapture(0)

CurrentColor = ""
LastColor = ""

broker = '10.100.20.142'
port = 1883
topic = "CubeColor"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

def publishColor(client):
    global LastColor
    global CurrentColor
    
    if(LastColor != CurrentColor):
        LastColor = CurrentColor
        currentColorJSON = json.dumps({"color": CurrentColor})
        client.publish("CubeColor", currentColorJSON, 0, True)
        print("Color published: " + CurrentColor)

def camStart(client):
    print("Start detecting colors!")
    while True:
      
        # capturing the current frame
        _, frame = vid.read()
      
        # setting values for base colors
        b = frame[:, :, :2]
        g = frame[:, :, 1:2]
        r = frame[:, :, 2:]
      
        # computing the mean
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)
      
        global CurrentColor
      
        # displaying the most prominent color
        # print(str(b_mean) + ' | ' + str(g_mean) + ' | ' + str(r_mean))
        if (b_mean > g_mean and b_mean > r_mean):
            CurrentColor = "Blue"
        elif (g_mean > r_mean and g_mean > b_mean):
            CurrentColor = "Green"
        else:
            CurrentColor = "Red"
            
        #print(CurrentColor)
        publishColor(client)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    def on_publish(client, userdata, result):
        print("Published")
        
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker, port)
    return client

def run():
    client = connect_mqtt()
    client.loop_start()
    
    if True:
        camStart(client)

run()
