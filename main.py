# -*- coding: utf-8 -*-
from threading import Thread

from utils.model.predict import predict


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


# 以下为用于多线程的函数
def predict_thread(sentence, label_cls="pred-text", highlight_cls="pred-text-highlight",
                   model="/model/torch_pretrained_bert_multi_label/tmp/self/", labels_threshold=-0.6,
                   highlight_threshold=0.01):
    """
    用于预测的多线程
    :param sentence: 语句
    :return: 预测结果：[标签列表, 加入标签类别的语句字符串]
    """
    return predict(sentence=sentence, label_cls=label_cls, highlight_cls=highlight_cls, model=model,
                   labels_threshold=labels_threshold, highlight_threshold=highlight_threshold)


if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    sentence = u"被告人周某在越野车内窃得黑色手机。祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重。"
    predict_thread = MultiThread(predict_thread, args=(sentence, "pred-text", "pred-text-highlight",
                                                       r"E:/PyCharmWorkspace/LegalJudgment/utils/model/torch_pretrained_bert_multi_label/tmp/self/",
                                                       -0.6, 0.01))
    predict_thread.start()
    predict_thread.join()
    labels, highlight_sentence = predict_thread.get_predict()
    print("*" * 10 + " labels " + "*" * 10)
    print(labels)
    print("*" * 10 + " sentence " + "*" * 10)
    print(highlight_sentence)
