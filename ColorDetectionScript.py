from paho.mqtt import client as mqtt_client
import random
import numpy as np
import cv2
import json
import socket
from threading import Thread

print("Loading Camera...")
vid = cv2.VideoCapture(0)
print("Camera loaded")

CurrentColor = []

def camStart():
    print("Start detecting colors!")
    while True:
        _, frame = vid.read()
        b = frame[:, :, :2]
        g = frame[:, :, 1:2]
        r = frame[:, :, 2:]
      
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)
      
        global CurrentColor
      
        CurrentColor = []
      
        CurrentColor.append(int(b_mean))
        CurrentColor.append(int(g_mean))
        CurrentColor.append(int(r_mean))
        
def startRGBServer():
    HOST = "0.0.0.0"
    PORT = 65432
    print("StartRGBServer...")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with  conn:
                print(f"Connection established with {addr}.")
                while True:
                    try:
                        data = conn.recv(1024).decode("ascii")
                        data = data.split(" ")
                        
                        if len(data)>0:
                            if data[0]=="get":
                                if len(data)>1:
                                    if data[1]=="color":
                                        color = CurrentColor
                                        print("Send Color...")
                                        conn.sendall(bytes(color))
                            if(data[0]=="close"):
                                s.close()
                                print(f"Connection with {addr} closed. ")
                                break
                    except socket.error as e:
                        s.close()
                        break
                

def run():
    RGBServer = Thread(target=startRGBServer)
    RGBServer.start()
    
    Cam = Thread(target=camStart)
    Cam.start()

run()
