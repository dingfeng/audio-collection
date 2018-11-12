# -*- coding: UTF-8 -*-
# filename: svm date: 2018/11/8 10:23  
# author: FD
import numpy as np
import os
import sklearn
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn import metrics

ch_map = {'h': 0, 'i': 1, 'j': 2, 'k': 3, 'm': 4, 'n': 5, 'u': 6}


def main():
    pass


def cross_test():
    global ch_map
    validate_rate = 0
    feature_dirs = ['../preprocess/semi_key_record_1_feature', '../preprocess/semi_key_record_1_test_feature']
    labels = []
    features = []
    ch_list = np.asarray(['h', 'i', 'j', 'k', 'm', 'n', 'u'])
    for feature_dir in feature_dirs:
        for label_name in os.listdir(feature_dir):
            label_path = os.path.join(feature_dir, label_name)
            for filename in os.listdir(label_path):
                filepath = os.path.join(label_path, filename)
                labels.append(ch_map[label_name])
                feature = np.load(filepath)['mfcc_data']
                features.append(feature)
    features = np.asarray(features)
    labels = np.asarray(labels)
    features = features.reshape((len(features), 26))[:, :13]
    minMaxScaler = preprocessing.MinMaxScaler()
    minMaxScaler.fit(features)
    features = minMaxScaler.transform(features)
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0, random_state=0)
    clf = svm.LinearSVC(max_iter=1000)
    predicted = cross_val_predict(clf, X_train, y_train, cv=10)
    # print('scores : {}'.format(scores))
    result = np.asarray([ch_list[y_train], ch_list[predicted]]).T
    print("correct part")
    corrects = []
    wrongs = []
    for item in result:
        if item[0] == item[1]:
            corrects.append(item)
        else:
            wrongs.append(item)
    print("corrects")
    corrects=np.asarray(corrects)
    corrects.sort(axis=0)
    print(corrects)
    print("wrongs")
    wrongs=np.asarray(wrongs)
    print(wrongs)

    print(metrics.accuracy_score(y_train, predicted))


def test():
    (train_features, train_labels), (validate_features, validate_labels) = get_data()
    train_features = train_features.reshapek((len(train_features), 26))[:, :13]
    validate_features = validate_features.reshape(len(validate_features), 26)[:, :13]
    minMaxScaler = preprocessing.MinMaxScaler()
    minMaxScaler.fit(train_features)
    train_features = minMaxScaler.transform(train_features)
    clf = svm.LinearSVC(max_iter=1000)
    clf.fit(train_features, train_labels)
    validate_features = minMaxScaler.transform(validate_features)
    labels = clf.predict(validate_features)
    result = np.asarray([validate_labels, labels]).transpose()
    total = len(result)
    count = 0
    for item in result:
        if item[0] == item[1]:
            count += 1
    print('accracy: {} \n data {}'.format(count / total, result))
    return


def get_data():
    global ch_map
    validate_rate = 0.2
    feature_dirs = ['../preprocess/semi_key_record_1_feature', '../preprocess/semi_key_record_1_test_feature']
    labels = []
    features = []

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


if __name__ == '__main__':
    # main()
    test()
