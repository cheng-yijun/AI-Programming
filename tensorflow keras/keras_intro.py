import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
# from keras.models import Sequential
# from keras.layers import Dense, Activation
from mpl_toolkits.axes_grid1 import make_axes_locatable

def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    if training:
        return train_images, train_labels
    else:
        return test_images, test_labels

def print_stats(images, labels):
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    hight = len(images[0])
    width = len(images[0])
    print(len(images))
    print(str(hight) + 'x' + str(width))
    num_label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(labels)):
        num_label[labels[i]] = num_label[labels[i]] + 1
    for i in range(10):
        print(str(i) + '. ' + class_names[i] + ' - ' + str(num_label[i]))

def view_image(image, label):
    fig, axes = plt.subplots(1, 1)
    img_orig = axes.imshow(image, aspect='equal')
    plt.show()
    axes.set_title(label)
    divider = make_axes_locatable(axes)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(img_orig, cax=cax)

def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(28, 28)))
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(10))
    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model, images, labels, T):
    model.fit(images, labels, epochs=T)

def evaluate_model(model, images, labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(x=images, y=labels, verbose=0)
    if show_loss:
        print('Loss: ' + str("{:.2}".format(test_loss)))
    print('Accuracy: ' + str("{:.2%}".format(test_accuracy)))

def predict_label(model, images, index):
    model.add(keras.layers.Softmax())
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