import tensorflow as tf
import numpy as np
import keras
import cv2
import glob
from helper import download, likes
import matplotlib.pyplot as plt

DESIRED_ACCURACY = 0.80


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('loss') is not None and logs.get('loss') <= DESIRED_ACCURACY:
            print("\nReached 65% accuracy so cancelling training!")
            self.model.stop_training = True


np.set_printoptions(linewidth=200)

np_likes = np.array(likes())  # print(np_likes)
norm = np.linalg.norm(np_likes)
np_likes_normalized = np_likes / norm  # print(np_likes_normalized)

data_directory = '../img'
images = []

for img in glob.glob(data_directory + "/*.jpeg"):
    image = cv2.imread(img)
    image_resized = cv2.resize(image, (128, 128))
    images.append(image_resized)

np_images = np.array(images)
np_images = np_images / 255.0

train_coverage = 0.6

x_train, y_train = np_images[:int(train_coverage * len(np_images))], np_likes_normalized[
                                                                     :int(train_coverage * len(np_images))]
x_test, y_test = np_images[int(train_coverage * len(np_images)):], np_likes_normalized[
                                                                   int(train_coverage * len(np_images)):]

callbacks = myCallback()

# print(x_train)
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(10, (5, 5), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.Conv2D(20, (5, 5), activation='relu'),
    tf.keras.layers.MaxPooling2D(3, 3),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(25, activation='relu'),
    tf.keras.layers.Dense(1, activation='softmax')
])

model.compile(optimizer='rmsprop', loss='mean_squared_logarithmic_error')

print(model.summary())

model.fit(x_train, y_train, epochs=10, callbacks=[callbacks], validation_data=(x_test, y_test), shuffle=True)
print(model.evaluate(x_test, y_test))

model.save('../model/model1.h')
