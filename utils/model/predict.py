# -*- coding: utf-8 -*-
from time import time

import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification


def __get_highlight_ids(attentions):
    threshold = 0.01  # FIXME 调整阈值
    attentions = list(attentions)
    attentions = [att.detach().numpy() for att in attentions]
    consider_layers_ids = [10]
    consider_layers = []
    for layer_id in consider_layers_ids:
        layer = attentions[layer_id]
        head = np.average(np.average(layer, axis=0), axis=0)
        to_consider_head = head[0:-1, 0:-1]
        consider_layers.append(to_consider_head)
    consider_layers = np.average(consider_layers, axis=0)
    cls2others = consider_layers[0, 1:]
    max_rate = cls2others.max()
    rate_threshold = max_rate * threshold
    huge_w_ids = list(np.where(cls2others >= rate_threshold)[0])
    return huge_w_ids


def __get_label_ids(preds):
    preds = preds.view(-1)
    threshold = -0.6  # FIXME 调整阈值
    preds_max = preds.max()
    preds_threshold = preds_max * threshold
    return list(np.where(preds > preds_threshold)[0])


def predict_ids(model_version, sentence):
    do_lower_case = True
    model = BertForSequenceClassification.from_pretrained(model_version, num_labels=202,
                                                          output_attentions=True)
    tokenizer = BertTokenizer.from_pretrained(model_version, do_lower_case=do_lower_case)
    max_seq_length = 256
    sentence = sentence[:max_seq_length]

    inputs = tokenizer.encode_plus(sentence, None, return_tensors='pt', add_special_tokens=True)
    token_type_ids = inputs['token_type_ids']
    input_ids = inputs['input_ids']

    preds, attentions = model(input_ids, token_type_ids=token_type_ids)

    preds_labels_ids = __get_label_ids(preds=preds)
    preds_highlight_ids = __get_highlight_ids(attentions=attentions)

    return preds_labels_ids, preds_highlight_ids


if __name__ == '__main__':
    model_version = r"E:/PyCharmWorkspace/LegalJudgment/utils/model/torch_pretrained_bert_multi_label/tmp/self/"
    sentence = u"被告人周某在越野车内窃得黑色手机。祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重。"
    start_time = time()
    label_ids, highlight_ids = predict_ids(model_version, sentence)
    end_time = time()
    print("*" * 10 + " label indices (suppose [190,1]) " + "*" * 10)
    print(label_ids)
    print("*" * 10 + " highlight indices " + "*" * 10)
    print(highlight_ids)
    print("*" * 10 + " cost time: %d s " % (end_time - start_time) + "*" * 10)
