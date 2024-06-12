import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import time

#load the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

#define the model
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10)
])

#compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#train the model and measure the training time
start_time = time.time()
model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))
end_time = time.time()

#evaluate the model
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

print(f"TensorFlow Training Time: {end_time - start_time} seconds")
print(f"TensorFlow Test Accuracy: {test_acc}")
