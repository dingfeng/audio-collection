# -*- coding: UTF-8 -*-
# filename: sklearn_svm date: 2018/11/5 11:57  
# author: FD 
from sklearn.svm import SVC
import numpy as np
import os
from sklearn.externals import joblib

feature_dir = '../collect_data/features'
filename = 'dingfeng_12_200hz.npz'
filepath = os.path.join(feature_dir, filename)
data = np.load(filepath)
tags = data['tags']
filenames = data['filenames']
mfcc_features = data['mfcc_features']
keys = [chr(i) for i in range(97, 123)]

if not os.path.isdir("sk_svm_models"):
    os.mkdir("sk_svm_models")

def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return [ backitems[i][1] for i in range(0,len(backitems))]

def get_clf(a, b):
    a_indices = np.where(tags == a)
    a_mfcc_features = mfcc_features[a_indices]
    a_y = [1 for i in range(len(a_mfcc_features))]
    b_indices = np.where(tags == b)
    b_mfcc_features = mfcc_features[b_indices]
    b_y = [0 for i in range(len(b_mfcc_features))]
    if (len(b_y) == 0 or len(a_y) == 0):
        return None
    clf = SVC(kernel='linear')
    X = np.concatenate((a_mfcc_features, b_mfcc_features), axis=0)
    y = a_y + b_y
    rf = clf.fit(X, y)
    if (clf is not None):
        print("dict_key {} precision {}".format(a + b, clf.score(X, y)))
    joblib.dump(rf, 'sk_svm_models/' + a + b + ".model")
    return clf


def create_clf_dict():
    clf_dict = {}
    keys_len = len(keys)
    for i in range(keys_len - 1):
        a = keys[i]
        for j in range(i + 1, keys_len):
            b = keys[j]
            dict_key = a + b
            clf_dict[dict_key] = get_clf(a, b)
    return clf_dict


def get_clf_dict():
    clf_dict = {}
    keys_len = len(keys)
    for i in range(keys_len - 1):
        a = keys[i]
        for j in range(i + 1, keys_len):
            b = keys[j]
            dict_key = a + b
            filepath = 'sk_svm_models/' + dict_key + ".model"
            if os.path.isfile(filepath):
                clf_dict[dict_key] = joblib.load(filepath)
    return clf_dict


def predict(clf_dict, mfcc_feature):
    scores = dict.fromkeys(keys, 0.0)
    keys_len = len(keys)
    for i in range(keys_len - 1):
        a = keys[i]
        for j in range(i + 1, keys_len):
            b = keys[j]
            dict_key = a + b
            if clf_dict.get(dict_key) is None:
                continue
            result = clf_dict[dict_key].predict(mfcc_feature)
            if (result >= 0.5):
                scores[a] += 1.0
            else:
                scores[b] += 1.0
    max_score_key = None
    max_score = -1
    for ch in scores.keys():
        score = scores[ch]
        if (score > max_score):
            max_score = score
            max_score_key = ch
    print("scores {}".format(sort_by_value(scores)))
    return max_score_key


if __name__ == '__main__':
    # create_clf_dict()
    clf_dict = get_clf_dict()
    filename = 'dingfeng_12_200hz_recent.npz'
    filepath = os.path.join(feature_dir, filename)
    data = np.load(filepath)
    tags = data['tags']
    filenames = data['filenames']
    mfcc_features = data['mfcc_features'].astype(np.float32)
    # a_indices = np.where(tags == 'b')
    # a_mfcc_features = mfcc_features[a_indices]
    # a_y = [1 for i in range(len(a_mfcc_features))]
    for index, item in enumerate(tags):
        mfcc_feature = mfcc_features[index]
        predict_result = predict(clf_dict, np.asarray([mfcc_feature]))
        # tag = a_y[index]
        # filename = filenames[index]
        print("tag {} predict_result {}".format(tags[index],predict_result))
