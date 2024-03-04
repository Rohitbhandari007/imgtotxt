from keras.models import load_model
from utils.losses import CTCloss
from metrics import CWERMetric
from keras.applications.inception_v3 import preprocess_input, decode_predictions, predict
from keras.preprocessing import load_image, image_to_array, expand_dims


def custom_load_model(model_path, img_path):
    """ Load the model with the custom_objects argument"""
    model = load_model(model_path, custom_objects={'CTCloss': CTCloss(), 'CWERMetric': CWERMetric})
    img = load_image(img_path, target_size=(224, 224))  
    img_array = image_to_array(img)
    img_array = expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = predict(model, img_array)
    decoded_predictions = decode_predictions(predictions)
    
    return decoded_predictions