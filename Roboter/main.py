import DoBotArm as Dbt
from paho.mqtt import client as mqtt_client
import random
import json

Color = None
    
def main():
    client = connect_mqtt()
    client.loop_start()
    
    print(Color)
    
    homeX, homeY, homeZ = 257, 4, 76, 
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    
    while True:
        
        if Color != None:
        
            input("Start:")
            
            GetCurrentColor()
        
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
            
def get_colour_name(b_mean, g_mean, r_mean):
    currentColor = ""
    # Bestimmt die prominenteste Farbe und setzt die Variable
    if (b_mean > g_mean and b_mean > r_mean) :
        currentColor = "blue"
    elif (g_mean > r_mean and g_mean > b_mean) :
        currentColor = "green”"
    else:
        currentColor = "red"
    return currentColor

def GetCurrentColor():
    HOST = "10.62.255.10" # The server's hostname or IP address
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                data = "get color"
                s.sendall(bytes(data, "ascii"))
                if(data=="close"):
                    print("closing...")
                    s.sendall(bytes("close", "ascii"))
                    s.close()
                    break;
                else:
                    data = s.recv(1024)
                    print([data[0], data[1], data[2]])
                    actual_name = get_colour_name(data[0], data[1], data[2])
                    Color = actual_name
                    return
            except KeyboardInterrupt:
                s.sendall(bytes("close", "ascii"))
                s.close()

main()



