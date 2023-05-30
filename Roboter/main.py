import DoBotArm as Dbt
from paho.mqtt import client as mqtt_client

Color = "Blue"
    
def main():
    homeX, homeY, homeZ = 257, 4, 76, 
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    
    while True:
        Color = input("Farbe: ")
        
        
        ctrlBot.toggleSuction()
        ctrlBot.moveArmXYZ(286,12,-36)
    
        ctrlBot.moveHome()
    
        if Color == "Red":
            ctrlBot.moveArmXYZ(182,190,-29)
        elif Color == "Blue":
            ctrlBot.moveArmXYZ(113,242,-32)
        else:
            ctrlBot.moveArmXYZ(39,275,-33)
        
        ctrlBot.toggleSuction()
        ctrlBot.moveHome()

main()

