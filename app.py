from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import io
from tflite_runtime.interpreter import Interpreter

app = Flask(__name__)

# load TFLite model and allocate tensors
TFLITE_MODEL_PATH = 'transfer_learning_model.tflite'
interpreter = Interpreter(model_path=TFLITE_MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_input(x):
    # minimal ResNet50 preprocessing: subtract mean RGB as in original ResNet50
    x = x.astype(np.float32)
    mean = np.array([103.939, 116.779, 123.68], dtype=np.float32)
    x[..., 0] -= mean[0]
    x[..., 1] -= mean[1]
    x[..., 2] -= mean[2]
    return x

def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image_array = np.asarray(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    image_array = image_array.astype(np.float32)
    return image_array

@app.route('/')
def index():
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
        processed_image = prepare_image(image, target_size=(224, 224))

        # set input tensor
        interpreter.set_tensor(input_details[0]['index'], processed_image)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])[0]

        # apply softmax manually (since tflite-runtime does not have tf.nn.softmax)
        exp_preds = np.exp(prediction - np.max(prediction))
        pred_prob = exp_preds / exp_preds.sum()
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