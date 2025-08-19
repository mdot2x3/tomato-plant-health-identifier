import tensorflow as tf

# load your Keras model
model = tf.keras.models.load_model('transfer_learning_model_saved.h5')

# convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# save the TFLite model
with open('transfer_learning_model.tflite', 'wb') as f:
    f.write(tflite_model)
