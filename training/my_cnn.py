# -*- coding: UTF-8 -*-
# filename: my_cnn date: 2018/11/7 14:27  
# author: FD 
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.utils import to_categorical
from keras.datasets import cifar10
import os

noClasses = 7
input_shape = ()


def main():
    global input_shape
    (train_features, train_labels), (validate_features, validate_labels) = get_data()
    nRows, nCols, nDims = train_features.shape[1:]
    input_shape = (nRows, nCols, nDims)
    train_labels_one_hot = to_categorical(train_labels)
    test_labels_one_hot = to_categorical(validate_labels)
    model1 = createModel()
    batch_size = 32
    epochs = 100
    model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model1.summary()

    history = model1.fit(train_features, train_labels_one_hot, batch_size=batch_size, epochs=epochs, verbose=1,
                         validation_data=(validate_features, test_labels_one_hot))
    model1.evaluate(validate_features, test_labels_one_hot)

    plt.figure(figsize=[8, 6])
    plt.plot(history.history['loss'], 'r', linewidth=3.0)
    plt.plot(history.history['val_loss'], 'b', linewidth=3.0)
    plt.legend(['Training loss', 'Validation Loss'], fontsize=18)
    plt.xlabel('Epochs ', fontsize=16)
    plt.ylabel('Loss', fontsize=16)
    plt.title('Loss Curves', fontsize=16)

    plt.figure(figsize=[8, 6])
    plt.plot(history.history['acc'], 'r', linewidth=3.0)
    plt.plot(history.history['val_acc'], 'b', linewidth=3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=18)
    plt.xlabel('Epochs ', fontsize=16)
    plt.ylabel('Accuracy', fontsize=16)
    plt.title('Accuracy Curves', fontsize=16)

    plt.show()
    return


def get_data():
    validate_rate = 0.2
    feature_dirs = ['../preprocess/semi_key_record_1_feature', '../preprocess/semi_key_record_1_test_feature']
    labels = []
    features = []
    ch_map = {'h': 0, 'i': 1, 'j': 2, 'k': 3, 'm': 4, 'n': 5, 'u': 6}
    for feature_dir in feature_dirs:
        for label_name in os.listdir(feature_dir):
            label_path = os.path.join(feature_dir, label_name)
            for filename in os.listdir(label_path):
                filepath = os.path.join(label_path, filename)
                labels.append(ch_map[label_name])
                feature = np.load(filepath)['mfcc_data']
                features.append(feature)
    indexes = np.arange(len(labels))
    np.random.shuffle(indexes)
    labels = np.asarray(labels)[indexes]
    features = np.asarray(features)[indexes].astype(np.float32)
    dividing_index = int(len(labels) * (1 - validate_rate))
    train_features = features[:dividing_index]
    train_labels = labels[:dividing_index]
    validate_features = features[dividing_index:]
    validate_labels = labels[dividing_index:]
    return (train_features, train_labels), (validate_features, validate_labels)


def createModel():
    global noClasses
    global input_shape
    model = Sequential()
    # The first two layers with 32 filters of window size 3x3
    model.add(Conv2D(32, (10, 2), padding='same', activation='tanh', input_shape=input_shape))
    model.add(Conv2D(32, (10, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 2), activation='relu'))
    model.add(Conv2D(64, (3, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 2)))
    model.add(Dropout(0.25))

    # model.add(Conv2D(64, (2, 2), padding='same', activation='relu'))
    # model.add(Conv2D(64, (2, 2), activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(noClasses, activation='softmax'))

    return model


if __name__ == '__main__':
    main()
