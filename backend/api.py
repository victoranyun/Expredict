import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

# loading the previously saved model
new_model = tf.keras.models.load_model('../model')

# checking if imports worked
print(new_model.summary())


def file_upload(req, folder):
    """
    Uploads multiple files and saves it to a folder on local disk
    :param req:
    :param folder:
    :return:
    """
    image_list = req.files.getlist("filename")
    full_file_paths = []
    for image in image_list:
        file_name = image.filename
        full_file_path = os.path.join(folder, file_name)
        image.save(full_file_path)
        full_file_paths.append(full_file_path)

    return full_file_paths


def resize(file_paths):
    """
    Resize the list of images in the file_path
    :param file_paths: a file_path with the .jpeg images
    :return: np array of resized images
    """
    image_list = []
    for image in file_paths:
        image_list.append(cv2.resize(cv2.imread(image), (128, 128)))
    return np.array(image_list)


def run_prediction(images):
    """
    Runs the prediction and evaluates the value
    :param images: np array of images
    :return: a sorted np array
    """
    images = images / 255.0
    prediction = new_model.predict(images)
    return np.argsort(prediction.flatten() * -1, kind='quicksort')  # sorting the array and collapsing into 1d


def find_max(predictions):
    """
    Find the first maximum from the left side of the flattened array
    :param predictions: array of sorted prediction values
    :return: index of first maximum that occurs (if multiple)
    """
    first_max = max(predictions)
    for i in predictions:
        if first_max == predictions[i]:
            return i


def display_image(np_array):
    """
    Displays the image
    :param np_array: np array of images
    :return: N/A
    """
    w, h = 128, 128
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[0:256, 0:256] = [255, 0, 0]
    img = Image.fromarray(np_array, 'RGB')
    img.save('best_image.png')
    img.show()



