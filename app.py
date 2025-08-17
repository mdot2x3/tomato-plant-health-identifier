from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image
import numpy as np
import io
import tensorflow as tf

app = Flask(__name__)

# load the trained model
model = load_model('transfer_learning_model_saved.h5')

# pre-processing function (same as in notebook)
def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image_array = np.asarray(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)  # use ResNet50 preprocessing
    return image_array

@app.route('/')
def index():
    # serve the main HTML page
    return render_template('index.html')

CLASS_LABELS = ['Bacterial_spot', 'Early_blight', 'healthy', 'Late_blight', 'Leaf_Mold', 'powdery_mildew', 'Septoria_leaf_spot',
        'Spider_mites Two-spotted_spider_mite', 'Target_Spot', 'Tomato_mosaic_virus', 'Tomato_Yellow_Leaf_Curl_Virus']

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # pre-process the image
        processed_image = prepare_image(image, target_size=(224, 224)) # use model's input size

        # make a prediction
        prediction = model.predict(processed_image)
        pred_prob = tf.nn.softmax(prediction[0]).numpy()  # apply softmax
        
        # format the response
        # depends heavily on the model's output
        predicted_class = int(np.argmax(pred_prob))
        confidence = float(np.max(pred_prob))
        label = CLASS_LABELS[predicted_class] if predicted_class < len(CLASS_LABELS) else f"Class {predicted_class}"

        return jsonify({
            "prediction": label,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)