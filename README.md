# Tomato Plant Health Identifier

A web application that uses a Convolutional Neural Network (CNN) to identify the health status and diseases of tomato plants from images.

## Features

The machine learning model is capable of identifying a healthy tomato leaf and tomato leaf diseases in the following 10 categories (bacterial spot, early blight, late blight, leaf mold, powdery mildew, septoria leaf spot, spider mites(two-spotted spider mite), target spot, tomato mosaic virus, tomato yellow leaf curl virus).

- Upload or capture an image of a (single preferably) tomato plant leaf for prediction (mobile-friendly: supports camera capture)
- Select from sample images using a dropdown for quick testing
- Predicts various tomato plant diseases and healthy status
- Built with Flask and TensorFlow Lite (TFLite)

## Setup (Local)

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/tomato-plant-health-identifier.git
   cd tomato-plant-health-identifier
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Add your trained model:**

   - Place your `.tflite` model file in the project root. This project uses the included ResNet50 transfer learning model `transfer_learning_model.tflite`.
   - If you need to convert a Keras `.h5` model to TFLite, use the provided `convert_to_tflite.py` script.

5. **Add sample images (optional but recommended):**
   - Place images you want available in the dropdown inside the `static/sample_images/` directory.

## Running the App Locally

```sh
python app.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Usage

- **Upload an image** or **take a photo** using the web interface.
- **Or, select a sample image from the dropdown and click "Predict".**
  - The dropdown is populated with images found in the `static/sample_images/` directory.
  - When you select a sample image, it will preview and can be submitted for prediction.
- The app will display the predicted class and confidence.

## Project Structure

- `app.py` - Main Flask application
- `convert_to_tflite.py` - Script to convert Keras `.h5` models to TFLite
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, sample images)
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku process file
- `transfer_learning_model.tflite` - Trained TFLite model file

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes
4. Push to your fork and open a pull request

## License

MIT License

## Acknowledgements

https://www.kaggle.com/datasets/ashishmotwani/tomato?select=train
