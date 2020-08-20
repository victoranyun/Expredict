import tensorflow as tf
import numpy as np
import keras
import cv2
import glob
from helper import download, likes
import matplotlib.pyplot as plt

DESIRED_ACCURACY = 0.65


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('acc') is not None and logs.get('acc') >= DESIRED_ACCURACY:
            print("\nReached 65% accuracy so cancelling training!")
            self.model.stop_training = True


np.set_printoptions(linewidth=200)

np_likes = np.array(likes())  # print(np_likes)
norm = np.linalg.norm(np_likes)
np_likes_normalized = np_likes / norm  # print(np_likes_normalized)

data_directory = '../img'
images = []

for img in glob.glob(data_directory + "/*.jpg"):
    image = cv2.imread(img)
    image_resized = cv2.resize(image, (100, 100))
    images.append(image_resized)

np_images = np.array(images)
np_images = np_images / 255.0

# for i in np_images:
#     print(i.shape)

train_coverage = 0.6

x_train, y_train = np_images[:int(train_coverage*len(np_images))], np_likes_normalized[:int(train_coverage*len(np_images))]
x_test, y_test = np_images[int(train_coverage*len(np_images)):], np_likes_normalized[int(train_coverage*len(np_images)):]

callbacks = myCallback()

print(x_train)
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
  tf.keras.layers.MaxPooling2D(5, 5),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(25, activation='relu'),
  tf.keras.layers.Dense(1, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

model.fit(x_train, y_train, epochs=5, callbacks=[callbacks], validation_data = (x_test, y_test))
print(model.evaluate(x_test, y_test))
