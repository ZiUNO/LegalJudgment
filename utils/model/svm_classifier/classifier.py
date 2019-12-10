import csv
import re
import sys
from datetime import datetime

import joblib
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

from utils.model.predict import Predict


class SVMClassifier(object):
    clf = None
    save_path = None

    @staticmethod
    def read_tsv(input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                if sys.version_info[0] == 2:
                    line = list(np.unicode(cell, 'utf-8') for cell in line)
                lines.append(line)
            return lines

    @staticmethod
    def tsv2dataset(tsv):
        datasets = {"X": [], "y": []}
        for i, line in enumerate(tsv):
            if i == 0:
                continue
            article = line[1][1:-1].split(',')
            article = list(set([int(i.strip()) for i in article]))
            article_ids = Predict.convert_article_to_ids(articles=article)
            charge = list(set(re.findall(u"'(.*?)'", line[2], re.S)))
            charge_ids = Predict.convert_charge_to_ids(charges=charge)
            datasets["X"].append(charge_ids)
            datasets["y"].append(article_ids)
        datasets["X"] = np.array(datasets["X"])
        datasets["y"] = np.array(datasets["y"])
        return datasets

    @classmethod
    def train(cls, train_datasets):
        X_train, y_train = train_datasets
        cls.clf = OneVsRestClassifier(SVC(gamma="auto"), n_jobs=-1) if cls.clf is None else cls.clf
        cls.clf.fit(X_train, y_train)
        return cls.clf

    @classmethod
    def load(cls, load_path=None, clf=None):
        if clf is not None:
            cls.clf = clf
        elif load_path is not None:
            cls.clf = joblib.load(load_path)
        else:
            raise ValueError("clf and load path should not be None at the same time")
        return cls.clf

    @classmethod
    def save(cls, clf=None, save_path=None):
        if save_path is None:
            raise ValueError("save path should not be empty")
        elif clf is not None:
            joblib.dump(clf, save_path)
            cls.clf = clf
        elif cls.clf is None:
            raise ValueError("cls.clf and clf should not be None at the same time")
        else:
            joblib.dump(cls.clf, save_path)

    @classmethod
    def predict(cls, X_test):
        return cls.clf.predict(X_test)

    @classmethod
    def score(cls, X, y):
        return cls.clf.score(X, y)


if __name__ == '__main__':
    path = r"E:/PyCharmWorkspace/LegalJudgment/utils/model/torch_pretrained_bert_multi_label/multi_data_dir/exercise_contest/"
    datasets = {"train": "train.tsv", "test": "test.tsv", "val": "val.tsv"}
    datasets = {key: path + datasets[key] for key in datasets}
    datasets = {key: SVMClassifier.tsv2dataset(SVMClassifier.read_tsv(datasets[key])) for key in datasets}
    X_train = datasets["train"]["X"]
    y_train = datasets["train"]["y"]
    X_test = datasets["test"]["X"]
    y_test = datasets["test"]["y"]

    pkl_path = "svm_clf.pkl"

    # train
    # start_time = time()
    # clf = SVMClassifier.train((X_train, y_train))
    # print("train cost time: %d(s)" % (time() - start_time))

    # save
    # SVMClassifier.save(save_path=pkl_path)

    # load
    start_time = datetime.now().microsecond
    clf = SVMClassifier.load(pkl_path)
    print("load cost time: %d(ms)" % (datetime.now().microsecond - start_time))

    # save-2
    SVMClassifier.save(save_path=pkl_path, clf=clf)

    # predict
    start_time = datetime.now().microsecond
    y_pred_0 = SVMClassifier.predict(X_test[0:1])
    print("predict once cost time: %d(ms)" % (datetime.now().microsecond - start_time))

    # compare y_test[0:1] with y_pred_0
    print("-" * 10 + " y_pred_0 " + "-" * 10)
    print(y_pred_0)
    print("-" * 10 + " y_test[0:1] " + "-" * 10)
    print(y_test[0:1])

    # print("-" * 20)
    # start_time = datetime.now().second
    # print("score: %f" % clf.score(X_test, y_test))
    # print("calculate score cost time: %d(s)" % (datetime.now().second - start_time))
