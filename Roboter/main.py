import DoBotArm as Dbt
    
def main():
    homeX, homeY, homeZ = 257, 4, 76, 
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ) #Create DoBot Class Object with home position x,y,z
    ctrlBot.toggleSuction()
    ctrlBot.moveArmXYZ(286,12,-36)
    
    ctrlBot.moveHome()
    
    ctrlBot.moveArmXYZ(-6,-270,125)
    ctrlBot.toggleSuction()

main()
