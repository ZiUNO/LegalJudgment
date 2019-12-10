# -*- coding: utf-8 -*-
from threading import Thread
from time import time
import os

from utils.model.predict import Predict


class MultiThread(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.__func = func
        self.__args = args

    def run(self):
        self.__result = self.__func(*self.__args)

    def get_prediction(self):
        try:
            return self.__result
        except Exception:
            return None


if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    sentence = u"被告人周某在越野车内窃得黑色手机。祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重。"
    config = {"model_version": os.path.join("utils", "model", "torch_pretrained_bert_multi_label", "tmp", "self"),
              "clf": os.path.join("utils", "model", "svm_classifier", "svm_clf.pkl"),
              "highlight_consider_layer_ids": (7, 10),
              # FIXME [highlight_consider_layer_ids] 0-11共12层，调整考虑的神经层下标数以调整高亮部分的位置
              "charge_labels_threshold": -0.6,
              "highlight_threshold": 0.01}
    # init
    start_time = time()
    Predict.init(config)
    print("initializer cost time: %.02f(s)" % (time() - start_time))

    # predict
    start_time = time()
    predict_thread = MultiThread(Predict.predict_charge_and_highlight, args=(sentence,
                                                                             {"label_type": "text",
                                                                              "label_cls": "pred-text",
                                                                              "highlight_cls": "pred-text-highlight",
                                                                              "highlight_label_type": "div"}))
    predict_thread.start()
    predict_thread.join()

    charge_labels, highlight_sentence = predict_thread.get_prediction()

    article_thread = MultiThread(Predict.predict_articles, args=(charge_labels,))
    article_thread.start()
    article_thread.join()

    articles = article_thread.get_prediction()
    print("*" * 10 + " charge labels " + "*" * 10)
    print(charge_labels)
    print("*" * 10 + " highlight sentence " + "*" * 10)
    print(highlight_sentence)
    print("*" * 10 + " articles " + "*" * 10)
    print(articles)
    print("*" * 10 + " predict cost time: %.02f(s)" % (time() - start_time) + "*" * 10)
