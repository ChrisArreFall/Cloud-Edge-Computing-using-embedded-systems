from flask import Flask, render_template , request , jsonify
import requests
from PIL import Image
import os , io , sys
import numpy as np 
import cv2
import base64
from mega import Mega
import time

app = Flask(__name__)

addrIM = 'http://image-processing-service:5001'
urlIM = addrIM + '/processBase64'

addrOB = 'http://object-recognition-service:5002'
urlOB = addrOB + '/predictBase64'

# prepare headers for http request
content_type = 'image/jpeg'

mega = Mega()
m = mega.login('chrisarredondo2017@gmail.com', '2016094916')

@app.route('/start' , methods=['POST'])
def start():
    file = request.files['image'].read() ## byte file
    print(request.form['option'])
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    
    ################################################
    if(request.form['option']=='object_detection'):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype("uint8"))
        rawBytes = io.BytesIO()
        img.save(rawBytes, "JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        response = requests.post(urlOB, json={'image': str(img_base64)})
        return response.text
    elif(request.form['option']=='save_image'):
        name = str(time.time())+".png"
        cv2.imwrite(name,img)
        file = m.upload(name)
        link = m.get_upload_link(file)

        os.remove(name)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype("uint8"))
        rawBytes = io.BytesIO()
        img.save(rawBytes, "JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        return jsonify({'status':str(img_base64),'link':str(link)})
    else:
        img = Image.fromarray(img.astype("uint8"))
        rawBytes = io.BytesIO()
        img.save(rawBytes, "JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        response = requests.post(urlIM, json={'image': str(img_base64),'operation':str(request.form['option'])})
        #print(response.text)
        return response.text


@app.route('/test' , methods=['GET','POST'])
def test():
    print("log: got at test" , file=sys.stderr)
    return jsonify({'status':'succces'})

@app.route('/home')
def home():
    return render_template('index.jinja2')


    
@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0', port=5000)