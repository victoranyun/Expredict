import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

new_model = tf.keras.models.load_model('../model/model1.h')

print(new_model.summary())

global graph


def resize(file_paths):
    image_list = []

    for image in file_paths:
        resized = cv2.resize(cv2.imread(image), (128, 128))
        image_list.append(resized)

    return np.array(image_list)


def run_prediction(images):
    images = images / 255.0
    prediction = new_model.predict(images)
    sorted_np = np.argsort(prediction.flatten() * -1)
    return sorted_np


def find_max(predictions):
    first_max = max(predictions)
    for i in predictions:
        if first_max == predictions[i]:
            return i


def display_image(np_array):
    w, h = 128, 128
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[0:256, 0:256] = [255, 0, 0]
    img = Image.fromarray(np_array, 'RGB')
    img.save('best_image.png')
    img.show()


