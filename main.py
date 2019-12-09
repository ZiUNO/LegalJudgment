# -*- coding: utf-8 -*-
from threading import Thread

from utils.model.predict import Predict


class MultiThread(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.__func = func
        self.__args = args

    def run(self):
        self.__result = self.__func(*self.__args)

    def get_predict(self):
        try:
            return self.__result
        except Exception:
            return None


if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    sentence = u"被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重。"
    predict_thread = MultiThread(Predict().predict_charge_and_highlight,
                                 args=(sentence, {"label_type": "div",
                                                  "label_cls": "pred-text",
                                                  "highlight_cls": "pred-text-highlight",
                                                  "highlight_label_type": "div",
                                                  "model": r"utils/model/torch_pretrained_bert_multi_label/tmp/self/",
                                                  "labels_threshold": -0.6,
                                                  "highlight_threshold": 0.01}))
    predict_thread.start()
    predict_thread.join()
    charge_labels, highlight_sentence = predict_thread.get_predict()
    print("*" * 10 + " charge labels " + "*" * 10)
    print(charge_labels)
    print("*" * 10 + " sentence " + "*" * 10)
    print(highlight_sentence)
