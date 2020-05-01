from __future__ import print_function
import requests
import json
import numpy as np
import cv2
from PIL import Image
import base64
import os , io , sys

addr = 'http://localhost:5000'
test_url = addr + '/processImage'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

# Used image to test 
img = cv2.imread('dog.jpg')

cv2.imshow('image',img)
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()

# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

# decode response
image = json.loads(response.text)
bytesdata = base64.b64decode(image["status"][2:len(image["status"])-1])


image_data = io.BytesIO(bytesdata)
image = Image.open(image_data)
image = cv2.cvtColor(np.array(image), cv2.IMREAD_COLOR)


