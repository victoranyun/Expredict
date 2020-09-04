import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import cv2

default_graph = tf.Graph()


def resize(file_paths):
    image_list = []

    for image in file_paths:
        resized = cv2.resize(cv2.imread(image), (128, 128))
        image_list.append(resized)

    return np.array(image_list)


def run_prediction(images):
    model = load_model("../model/model.h")
