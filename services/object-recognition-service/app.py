# Submit a request via cURL:
# 	curl -X POST -F image=@ppicture.jpg 'http://localhost:5000/predict'
# import the necessary packages
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from flask import Flask, request, Response,make_response, jsonify
import base64
import io
import tensorflow as tf

# initialize Flask application
app = Flask(__name__)
# initialize Keras model
model = None

def load_model():
	# load the pre-trained Keras model.
	global model
	# Interchangable
	model = ResNet50(weights="imagenet")
	global graph
	graph = tf.get_default_graph()

def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if request.method == "POST":
		if request.files.get("image"):
			# read the image in PIL format
			image = request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			image = prepare_image(image, target=(224, 224))

			# classify the input image and then initialize the list
			# of predictions to return to the client
			with graph.as_default():
				preds = model.predict(image)
				results = imagenet_utils.decode_predictions(preds)
				data["predictions"] = []

				# loop over the results and add them to the list of
				# returned predictions
				for (imagenetID, label, prob) in results[0]:
					r = {"label": label, "probability": float(prob)}
					data["predictions"].append(r)

				# indicate that the request was a success
				data["success"] = True

	# return the data dictionary as a JSON response
	return jsonify(data)


@app.route("/predictBase64", methods=["POST"])
def predictBase64():
	data = request.json
	bytesdata = base64.b64decode(data["image"][2:len(data["image"])-1])
	image_data = io.BytesIO(bytesdata)
	image = Image.open(image_data)

	# preprocess the image and prepare it for classification
	image = prepare_image(image, target=(224, 224))

	# classify the input image and then initialize the list
	# of predictions to return to the client
	with graph.as_default():
		preds = model.predict(image)
		results = imagenet_utils.decode_predictions(preds)
		data["predictions"] = []

		# loop over the results and add them to the list of
		# returned predictions
		for (imagenetID, label, prob) in results[0]:
			r = {"label": label, "probability": float(prob)}
			data["predictions"].append(r)

	# return the data dictionary as a JSON response
	print(data["predictions"])
	return jsonify({'status':data["image"],'predictions':data["predictions"]})

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run(host='0.0.0.0', port=5002)
