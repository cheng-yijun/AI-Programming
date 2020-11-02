import tensorflow as tf
from tensorflow import keras
import numpy as np

def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    train_images = np.expand_dims(train_images, axis=3)
    test_images = np.expand_dims(test_images, axis=3)
    if training:
        return train_images, train_labels
    else:
        return test_images, test_labels

def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(64, 3, activation='relu', input_shape=(28, 28, 1)))
    model.add(keras.layers.Conv2D(32, 3, activation='relu'))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(10, 'softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model, train_img, train_lab, test_img, test_lab, T):
    train_lab = keras.utils.to_categorical(train_lab)
    test_lab = keras.utils.to_categorical(test_lab)
    model.fit(train_img, train_lab, epochs=T, validation_data=(test_img, test_lab))
    # test_loss, test_accuracy = model.evaluate(x=test_img, y=test_lab, verbose=0)

def predict_label(model, images, index):
    predict = model.predict(images)
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    tmp_pred = []
    for i in range(10):
        tmp_pred.append(predict[index][i])

    idx = 0
    max1 = -1
    for i in range(10):
        if tmp_pred[i] > max1:
            max1 = tmp_pred[i]
            idx = i
    max2 = -1
    idx2 = 0
    for i in range(9):
        if tmp_pred[i] > max2 and tmp_pred[i] != max1:
            max2 = tmp_pred[i]
            idx2 = i
    max3 = -1
    idx3 = 0
    for i in range(8):
        if tmp_pred[i] > max3 and tmp_pred[i] != max1 and tmp_pred[i] != max2:
            max3 = tmp_pred[i]
            idx3 = i

    print(class_names[idx] + ': ' + str("{:.2%}".format(max1)))
    print(class_names[idx2] + ': ' + str("{:.2%}".format(max2)))
    print(class_names[idx3] + ': ' + str("{:.2%}".format(max3)))