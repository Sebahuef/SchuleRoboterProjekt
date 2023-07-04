import socket
import adafruit_dht
import board
from threading import Thread
import time

def getCurrentTemperatur():   
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    
    def checkTemperatur():
        for i in range(10):
            try:
                return int(dhtDevice.temperature)
            except RuntimeError:
                print("hallo")
                
            time.sleep(3)
    
    print(checkTemperatur())
    
    return checkTemperatur()

def startTempServer():
    HOST = "0.0.0.0"
    PORT = 65432
    print("StartTempServer...")
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
                                    if data[1]=="temp":
                                        temp = getCurrentTemperatur()
                                        print("Send Temperatur...")
                                        conn.sendall(temp.to_bytes(2, 'big'))
                            if(data[0]=="close"):
                                s.close()
                                print(f"Connection with {addr} closed. ")
                                break
                    except socket.error as e:
                        s.close()
                        break

def run():
    startTempServer()
    
run()
