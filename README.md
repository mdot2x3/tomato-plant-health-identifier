# Tomato Plant Health Identifier

A web application that uses a Convolutional Neural Network (CNN) to identify the health status and diseases of tomato plants from images.

## Features

- Upload or capture an image for prediction
- Predicts various tomato plant diseases and healthy status
- Built with Flask and TensorFlow/Keras

## Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/tomato-plant-health-identifier.git
   cd tomato-plant-health-identifier
   ```

2. **Create and activate a virtual environment:**

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Add your trained model:**
   - Place your `model.h5` file in the project root. This project used the included ResNet50 transfer learning model `transfer_learning_model_saved.h5`.

## Running the App

```
python app.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Usage

- **Upload an image** or **take a photo** using the web interface.
- Or, select a sample image from the dropdown and click "Predict".
- The app will display the predicted class and confidence.

## Project Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS)
- `sample_images/` - Sample images for testing
- `requirements.txt` - Python dependencies

## License

MIT License
