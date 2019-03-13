import numpy as np 
from PIL import Image
from io import BytesIO
import base64

from keras.models import load_model, Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

model = load_model('cnn.h5')
model._make_predict_function()

def handle_image(data_url):

    '''
    Transforms image from POST request into appropriate format for
    Convolutional Neural Network

    @param str data_url: url from the post request
    @return PIL Image data type
    '''

    offset = data_url.index(',') + 1

    img_bytes = base64.b64decode(data_url[offset:])

    img = Image.open(BytesIO(img_bytes))

    img = img.convert(mode='L')

    img = img.resize((28,28), resample=Image.LANCZOS)

    img = np.asarray(img)
    img = img.astype('float64')
    img = img.reshape(-1,28,28,1)

    return img

def predict(img):

    global model

    model_softmax = model.predict(img)

    return np.argmax(model_softmax), model_softmax

