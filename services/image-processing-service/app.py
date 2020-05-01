from flask import Flask, request, Response,make_response, jsonify
import jsonpickle
import numpy as np
import cv2
import base64
from PIL import Image
import os , io , sys


# Initialize the Flask application
app = Flask(__name__)



@app.route('/processImage' , methods=['POST'])
def mask_image():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    ######### Do preprocessing here ################
    # img[img > 150] = 0
    ## any random stuff do here
    imageProcessing(img,1)
    ################################################
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({'status':str(img_base64)})

def imageProcessing(image,mode):
    if(mode == 1):
        #some processing
    elif(mode == 2):
        #some processing
    elif(mode == 3):
        #some processing
    elif(mode == 4):
        #some processing
    return image



# start flask app
app.run(host="0.0.0.0", port=5000)