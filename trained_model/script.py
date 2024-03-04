from utils.loaders import custom_load_model

def useModal(image):
    model = custom_load_model('model.h5', image)
    return model
