from flask import Flask, request, Response,make_response, jsonify
import jsonpickle
import numpy as np
import cv2
import base64
from PIL import Image
import os , io , sys
import json


# Initialize the Flask application
app = Flask(__name__)


@app.route('/processBase64' , methods=['POST'])
def processBase64():
    data = request.json
    bytesdata = base64.b64decode(data["image"][2:len(data["image"])-1])
    image_data = io.BytesIO(bytesdata)
    image = Image.open(image_data)
    image = cv2.cvtColor(np.array(image), cv2.IMREAD_COLOR)
    image = imageProcessing(image,data["operation"])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image.astype("uint8"))
    rawBytes = io.BytesIO()
    image.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({'status':str(img_base64)})

@app.route('/processImage' , methods=['POST'])
def processImage():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)

    imageProcessing(img,1)
    
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({'status':str(img_base64)})

def imageProcessing(image,mode):
    if(mode == "black_white"):
        print("Operation: Black and White")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    elif(mode == "denoise"):
        print("Operation: Denoise")
        image = cv2.fastNlMeansDenoisingColored(image,None,20,10,7,21) 
    elif(mode == "gaussian_blur"):
        print("Operation: Gaussian Blur")
        image = cv2.GaussianBlur(image, (7,7), 0) 
    elif(mode == "median_blur"):
        print("Operation: Median Blur")
        image = cv2.medianBlur(image,5) 
    elif (mode == "detect_edges"):
        print("Operation: Detect edges")
        image = cv2.Canny(image,100,200) 
    elif (mode == "color_detection"):
        print("Operation: Color Detection")
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([34, 177, 76])
        upper_green = np.array([255, 255, 255])
        image = cv2.inRange(hsv_img, lower_green, upper_green) 
    return image



# start flask app
app.run(host="0.0.0.0", port=5001)