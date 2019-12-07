# -*- coding: utf-8 -*-
import numpy as np
import torch
from transformers import BertTokenizer

from utils.model.torch_pretrained_bert_multi_label.run_classifier_multi_label import \
    BertForMultiLabelSequenceClassification, SelfProcessor


def predict(model_version, sentence):
    do_lower_case = True
    processor = SelfProcessor()
    label_list = processor.get_labels()
    model = BertForMultiLabelSequenceClassification.from_pretrained(model_version, num_labels=len(label_list))
    tokenizer = BertTokenizer.from_pretrained(model_version, do_lower_case=do_lower_case)
    max_seq_length = 256
    sentence = sentence[:max_seq_length]
    # device = torch.device("cuda")
    #
    # model.to(device)
    model.eval()

    tokens = tokenizer.tokenize(sentence)
    tokens = ["[CLS]"] + tokens + ["[SEP]"]
    segment_ids = [0] * len(tokens)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    input_mask = [1] * len(input_ids)

    padding = [0] * (max_seq_length - len(input_ids))
    input_ids += padding
    input_mask += padding
    segment_ids += padding

    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    batch = [input_ids, input_mask, segment_ids]
    batch = [torch.tensor([t]) for t in batch]
    # batch = tuple(t.to(device) for t in batch)
    input_ids, input_mask, segment_ids = batch

    with torch.no_grad():
        preds = model(input_ids, segment_ids, input_mask, labels=None)
    preds = preds.view(-1).numpy()
    threshold = - 0.8  # FIXME 调整阈值
    preds_max = preds.max()
    preds_threshold = preds_max * threshold
    preds_labels_ids = list(np.where(preds > preds_threshold)[0])

    preds_labels = [label_list[ids] for ids in preds_labels_ids]
    return preds_labels


if __name__ == '__main__':
    model_version = r"E:/PyCharmWorkspace/LegalJudgment/utils/model/torch_pretrained_bert_multi_label/tmp/self/"
    sentence = u"祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重，其行为已触犯了《中华人民共和国刑法》××××、××××第（一）、（二）、（三）项的规定，应当以××罪、××罪追究被告人李某的刑事责任。被告人李某犯数罪，应当数罪并罚。被告人李某在××刑罚执行完毕后在五年以内再犯应当判处××以上刑罚之罪，系累犯。提请本院依法判处。"
    result = predict(model_version, sentence)
    print(result)

# 祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重，其行为已触犯了《中华人民共和国刑法》××××、××××第（一）、（二）、（三）项的规定，应当以××罪、××罪追究被告人李某的刑事责任。被告人李某犯数罪，应当数罪并罚。被告人李某在××刑罚执行完毕后在五年以内再犯应当判处××以上刑罚之罪，系累犯。提请本院依法判处。	[293, 234]	['故意伤害', '寻衅滋事']	0	['李某']	False	108	False
