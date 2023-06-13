from paho.mqtt import client as mqtt_client
import random
import numpy as np
import cv2
import json
import socket

print("Loading Camera...")
vid = cv2.VideoCapture(0)

CurrentColor = ""

def camStart():
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
        
def startRGBServer():
    HOST = "0.0.0.0"
    PORT = 65432
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
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
                                        print("Processing image...")
                                        print("Dominant color: ")
                                        print(color)
                                        conn.sendall(bytes(color))
                            if(data[0]=="close"):
                                s.close()
                                print(f"Connection with {addr} closed. ")
                                break
                    except socket.error as e:
                        s.close()
                        break
                

def run():
    startRGBServer()
    camStart()

run()
