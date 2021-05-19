import tensorflow as tf
import numpy as np
import cv2
import glob
import json


DESIRED_ACCURACY = 0.9999
USERNAMES = open('../scraper/usernames.txt', 'r').read()
IMG_DIRECTORY = "../data/img/"
IMG_EXTENSION = "*.jpeg"


class myCallback(tf.keras.callbacks.Callback):
    """
    Ends training at a certain DESIRED_ACCURACY on epoch end
    """
    def on_epoch_end(self, epoch, logs={}):
        if logs['loss'] is not None and logs['loss'] <= DESIRED_ACCURACY:
            print("\nReached 99.9% accuracy so cancelling training!")
            self.model.stop_training = True


np.set_printoptions(linewidth=200)  # pretty print numpy array

np_likes = []
with open('../data/data.json') as json_file:
    data = json.load(json_file)
    for i in data[USERNAMES]:
        np_likes.append(i['likes_count'])

norm = np.linalg.norm(np_likes)  # return the norm of the vector (2-norm)
np_likes_normalized = np_likes / norm  # divide all by norm to normalize data for likes

images = []  # declaring array for images
for img in glob.glob(IMG_DIRECTORY + IMG_EXTENSION):  # unix style pathname recognition
    image = cv2.imread(img)  # load image into opencv
    images.append(cv2.resize(image, (128, 128)))  # add the resized images to images[]

np_images = np.array(images)  # creating np array for the images for processing
# np_images = np_images / 255.0  # normalizing pixel data for the images

train_coverage = 0.8  # train coverage , e.g. 60% train coverage = 60% training set and 40% testing set

# slicing the training/testing sets for training/testing
x_train, y_train = np_images[:int(train_coverage * len(np_images))], np_likes_normalized[
                                                                     :int(train_coverage * len(np_images))]
x_test, y_test = np_images[int(train_coverage * len(np_images)):], np_likes_normalized[
                                                                   int(train_coverage * len(np_images)):]

callbacks = myCallback()  # instantiating my epoch end callback class

model = tf.keras.models.Sequential([  # declaring the model layers
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.Conv2D(128, (5, 5), activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='mean_squared_error')  # using mean squared error to see how close regression
                                                            # is to points
print(model.summary())  # print model summary to see layer changes

# fit the model on the training data across 10 epochs (won't need for the desired accuracy)
model.fit(x_train, y_train, epochs=10, callbacks=[callbacks], validation_data=(x_test, y_test))

# save the model for using it later
model.save('../model')
