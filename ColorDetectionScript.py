import cv2
import numpy as np
from flask import Flask
  
CurrentColor = ""
  
def APISetup():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello, World!"
    
APISetup()

# taking the input from webcam
vid = cv2.VideoCapture(1)
  
# running while loop just to make sure that
# our program keep running until we stop it
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
  
    # displaying the most prominent color
    print(str(b_mean) + ' | ' + str(g_mean) + ' | ' + str(r_mean))
    if (b_mean > g_mean and b_mean > r_mean):
        CurrentColor = "Blue"
    elif (g_mean > r_mean and g_mean > b_mean):
        CurrentColor = "Green"
    else:
        CurrentColor = "Red"
        
