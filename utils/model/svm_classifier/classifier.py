import csv
import re
import sys
from datetime import datetime
from time import time

import joblib
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC, SVR

from utils.model.predict import Predict


class SVM(object):
    PREDS = {
        "article": 1,
        "imprisonment": 6,
        "single_label": 6,
    }
    model = None
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
    def tsv2dataset(tsv, pred_type):
        datasets = {"X": [], "y": []}
        for i, line in enumerate(tsv):
            if i == 0:
                continue
            if pred_type == "article":
                article = line[SVMClassifier.PREDS[pred_type]][1:-1].split(',')
                article = list(set([int(i.strip()) for i in article]))
                article_ids = Predict.convert_article_to_ids(articles=article)
                datasets["y"].append(article_ids)
            elif pred_type == "imprisonment":
                death_penality = True if line[5] == "True" else False
                life_imprisonment = True if line[7] == "True" else False
                imprison = float(
                    line[SVM.PREDS[pred_type]]) + death_penality * 30.0 * 12 + life_imprisonment * 20.0 * 12
                datasets["y"].append(imprison)
            elif pred_type == "single_label":
                death_penality = True if line[5] == "True" else False
                life_imprisonment = True if line[7] == "True" else False
                imprison = float(line[SVM.PREDS[pred_type]])
                imprison = 2 if death_penality or life_imprisonment or (imprison >= 10 * 12.0) else (
                    1 if 3 * 12.0 <= imprison < 10 * 12.0 else 0)
                # 2:  长期（10年以上/无期/死刑） 1： 中期（3年以上10年以下） 0： 短期（3年以下）

                datasets["y"].append(imprison)
            charge = list(set(re.findall(u"'(.*?)'", line[2], re.S)))
            charge_ids = Predict.convert_charge_to_ids(charges=charge)
            datasets["X"].append(charge_ids)

        datasets["X"] = np.array(datasets["X"])
        datasets["y"] = np.array(datasets["y"])
        return datasets

    @classmethod
    def load(cls, load_path=None, model=None):
        if model is not None:
            cls.model = model
        elif load_path is not None:
            cls.model = joblib.load(load_path)
        else:
            raise ValueError("clf and load path should not be None at the same time")
        return cls.model

    @classmethod
    def save(cls, model=None, save_path=None):
        if save_path is None:
            raise ValueError("save path should not be empty")
        elif model is not None:
            joblib.dump(model, save_path)
            cls.model = model
        elif cls.model is None:
            raise ValueError("cls.clf and clf should not be None at the same time")
        else:
            joblib.dump(cls.model, save_path)

    @classmethod
    def train(cls, train_datasets):
        raise NotImplementedError()

    @classmethod
    def predict(cls, X_test):
        return cls.model.predict(X_test)

    @classmethod
    def score(cls, X, y):
        return cls.model.score(X, y)


class SVMRegression(SVM):

    @classmethod
    def train(cls, train_datasets):
        X_train, y_train = train_datasets
        cls.model = GridSearchCV(SVR(gamma="auto"),
                                 param_grid={"kernel": ("linear", 'rbf'),
                                             "C": np.logspace(-3, 3, 7),
                                             "gamma": np.logspace(-3, 3, 7)},
                                 n_jobs=-1) if cls.model is None else cls.model
        cls.model.fit(X=X_train, y=y_train)
        return cls.model


class SVMClassifier(SVM):

    @classmethod
    def train(cls, train_datasets):
        X_train, y_train = train_datasets
        cls.model = OneVsRestClassifier(SVC(gamma="auto"), n_jobs=-1) if cls.model is None else cls.model
        cls.model.fit(X_train, y_train)
        return cls.model


class SVMSingleLabelClassifier(SVM):

    @classmethod
    def train(cls, train_datasets):
        X_train, y_train = train_datasets
        cls.model = SVC() if cls.model is None else cls.model
        cls.model.fit(X_train, y_train)
        return cls.model


if __name__ == '__main__':
    path = r"E:/PyCharmWorkspace/LegalJudgment/utils/model/torch_pretrained_bert_multi_label/multi_data_dir/exercise_contest/"
    # # dataset file name dict
    # clf_datasets = {"train": "train.tsv", "test": "test.tsv", "val": "val.tsv"}
    # reg_datasets = {"train": "train.tsv", "test": "test.tsv", "val": "val.tsv"}
    single_label_clf_datasets = {"train": "train.tsv", "test": "test.tsv", "val": "val.tsv"}

    # # dataset path dict
    # clf_datasets = {key: path + clf_datasets[key] for key in clf_datasets}
    # reg_datasets = {key: path + reg_datasets[key] for key in reg_datasets}
    single_label_clf_datasets = {key: path + single_label_clf_datasets[key] for key in single_label_clf_datasets}

    # # dataset dict
    # clf_datasets = {key: SVMClassifier.tsv2dataset(SVMClassifier.read_tsv(clf_datasets[key]), "charge") for key in
    #                 clf_datasets}
    # reg_datasets = {key: SVM.tsv2dataset(SVM.read_tsv(
    #     reg_datasets[key]), "imprisonment") for key in reg_datasets}
    single_label_clf_datasets = {key: SVM.tsv2dataset(SVM.read_tsv(single_label_clf_datasets[key]),
                                                      "single_label") for key in single_label_clf_datasets}

    # # train & test datasets
    # X_train = clf_datasets["train"]["X"]
    # y_train = clf_datasets["train"]["y"]
    # X_test = clf_datasets["test"]["X"]
    # y_test = clf_datasets["test"]["y"]
    # X_train = reg_datasets["train"]["X"]
    # y_train = reg_datasets["train"]["y"]
    # X_test = reg_datasets["test"]["X"]
    # y_test = reg_datasets["test"]["y"]
    X_train = single_label_clf_datasets["train"]["X"]
    y_train = single_label_clf_datasets["train"]["y"]
    X_test = single_label_clf_datasets["test"]["X"]
    y_test = single_label_clf_datasets["test"]["y"]

    # pkl_path = "svm_reg.pkl"
    # pkl_path = "svm_clf.pkl"
    pkl_path = "svm_single_label_clf.pkl"

    # train
    start_time = time()
    # model = SVMClassifier.train((X_train, y_train))
    # model = SVMRegression.train((X_train, y_train))
    model = SVMSingleLabelClassifier.train((X_train, y_train))

    print("train cost time: %.02f(s)" % (time() - start_time))

    # save
    SVM.save(save_path=pkl_path, model=model)

    # load
    # start_time = datetime.now().microsecond
    # model = SVM.load(load_path=pkl_path)
    # print("load cost time: %d(ms)" % (datetime.now().microsecond - start_time))

    # predict
    start_time = time()
    # y_pred_0 = SVMClassifier.predict(X_test[0:1])
    y_pred_0 = SVM.predict(X_test[0:1])
    print("predict once cost time: %.02f(s)" % (time() - start_time))

    # compare y_test[0:1] with y_pred_0
    print("-" * 10 + " y_pred_0 " + "-" * 10)
    print(y_pred_0)
    print("-" * 10 + " y_test[0:1] " + "-" * 10)
    print(y_test[0:1])

    print("-" * 20)
    start_time = time()
    print("score: %f" % SVM.score(X_test, y_test))
    print("calculate score cost time: %f(s)" % (time() - start_time))
