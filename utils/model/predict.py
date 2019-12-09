# -*- coding: utf-8 -*-
import re
from time import time

import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification


class Predict(object):
    @staticmethod
    def __get_charge_labels():
        """
        获取罪名标签
        :return: 罪名标签列表
        """
        return ["妨害公务", "寻衅滋事", "盗窃、侮辱尸体", "危险物品肇事", "非法采矿", "组织、强迫、引诱、容留、介绍卖淫", "开设赌场", "聚众斗殴", "绑架", "非法持有毒品",
                "销售假冒注册商标的商品", "容留他人吸毒", "假冒注册商标", "交通肇事", "破坏电力设备", "组织卖淫", "合同诈骗", "走私武器、弹药",
                "抢劫", "非法处置查封、扣押、冻结的财产", "以危险方法危害公共安全", "过失投放危险物质", "非法制造、买卖、运输、邮寄、储存枪支、弹药、爆炸物", "伪造、变造、买卖武装部队公文、证件、印章",
                "持有、使用假币", "重婚", "聚众冲击国家机关", "生产、销售伪劣农药、兽药、化肥、种子", "收买被拐卖的妇女、儿童", "聚众哄抢", "重大劳动安全事故", "侵占", "包庇毒品犯罪分子",
                "虚报注册资本", "违法发放贷款", "制造、贩卖、传播淫秽物品", "窝藏、包庇", "帮助毁灭、伪造证据", "放火", "强奸", "非法携带枪支、弹药、管制刀具、危险物品危及公共安全",
                "伪造、变造金融票证", "爆炸", "玩忽职守", "对非国家工作人员行贿", "伪造、倒卖伪造的有价票证", "私分国有资产", "非法收购、运输、加工、出售国家重点保护植物、国家重点保护植物制品",
                "生产、销售假药", "挪用特定款物", "过失致人死亡", "走私国家禁止进出口的货物、物品", "非法制造、买卖、运输、储存危险物质", "洗钱", "骗取贷款、票据承兑、金融票证",
                "非法买卖制毒物品", "非法买卖、运输、携带、持有毒品原植物种子、幼苗", "生产、销售有毒、有害食品", "滥用职权", "招收公务员、学生徇私舞弊", "诬告陷害", "非法获取国家秘密",
                "非法行医", "非法收购、运输、出售珍贵、濒危野生动物、珍贵、濒危野生动物制品", "非法出售发票", "行贿", "高利转贷", "非法吸收公众存款", "传播淫秽物品", "非法进行节育手术",
                "盗伐林木", "聚众扰乱社会秩序", "走私、贩卖、运输、制造毒品", "滥伐林木", "赌博", "非法经营", "生产、销售不符合安全标准的食品", "提供侵入、非法控制计算机信息系统程序、工具",
                "倒卖文物", "窃取、收买、非法提供信用卡信息", "盗掘古文化遗址、古墓葬", "协助组织卖淫", "破坏广播电视设施、公用电信设施", "走私普通货物、物品", "逃税", "破坏监管秩序",
                "失火", "受贿", "组织、领导、参加黑社会性质组织", "票据诈骗", "非法制造、销售非法制造的注册商标标识", "侵犯著作权", "伪造、变造、买卖国家机关公文、证件、印章",
                "徇私舞弊不征、少征税款", "强迫劳动", "贷款诈骗", "劫持船只、汽车", "诈骗", "非法种植毒品原植物", "非法狩猎", "挪用资金", "非法收购、运输盗伐、滥伐的林木",
                "出售、购买、运输假币", "抢夺", "虐待被监管人", "窝藏、转移、收购、销售赃物", "破坏计算机信息系统", "制作、复制、出版、贩卖、传播淫秽物品牟利", "拒不支付劳动报酬",
                "盗窃、抢夺枪支、弹药、爆炸物", "强迫他人吸毒", "走私珍贵动物、珍贵动物制品", "虐待", "非法获取公民个人信息", "破坏交通设施", "非法转让、倒卖土地使用权", "非法捕捞水产品",
                "非法占用农用地", "非法制造、出售非法制造的发票", "非法持有、私藏枪支、弹药", "集资诈骗", "强迫卖淫", "伪造公司、企业、事业单位、人民团体印章", "利用影响力受贿",
                "编造、故意传播虚假恐怖信息", "介绍贿赂", "传播性病", "拐卖妇女、儿童", "倒卖车票、船票", "窝藏、转移、隐瞒毒品、毒赃", "徇私舞弊不移交刑事案件",
                "过失损坏广播电视设施、公用电信设施", "动植物检疫徇私舞弊", "破坏交通工具", "猥亵儿童", "挪用公款", "伪造货币", "冒充军人招摇撞骗", "非法采伐、毁坏国家重点保护植物",
                "故意毁坏财物", "非法拘禁", "招摇撞骗", "伪造、变造居民身份证", "徇私枉法", "非法生产、买卖警用装备", "掩饰、隐瞒犯罪所得、犯罪所得收益", "生产、销售伪劣产品",
                "破坏生产经营", "帮助犯罪分子逃避处罚", "贪污", "投放危险物质", "持有伪造的发票", "危险驾驶", "妨害作证", "非法猎捕、杀害珍贵、濒危野生动物", "重大责任事故", "诽谤",
                "虚开发票", "引诱、教唆、欺骗他人吸毒", "脱逃", "扰乱无线电通讯管理秩序", "保险诈骗", "非法生产、销售间谍专用器材", "非法组织卖血", "强迫交易", "串通投标",
                "破坏易燃易爆设备", "传授犯罪方法", "妨害信用卡管理", "拐骗儿童", "单位行贿", "打击报复证人", "拒不执行判决、裁定", "经济犯", "金融凭证诈骗",
                "虚开增值税专用发票、用于骗取出口退税、抵扣税款发票", "走私废物", "组织、领导传销活动", "单位受贿", "盗窃、抢夺枪支、弹药、爆炸物、危险物质", "过失以危险方法危害公共安全",
                "过失致人重伤", "引诱、容留、介绍卖淫", "遗弃", "走私", "信用卡诈骗", "对单位行贿", "故意杀人", "聚众扰乱公共场所秩序、交通秩序", "盗窃", "故意伤害", "非法侵入住宅",
                "强制猥亵、侮辱妇女", "伪证", "污染环境", "巨额财产来源不明", "非国家工作人员受贿", "侮辱", "隐匿、故意销毁会计凭证、会计帐簿、财务会计报告",
                "过失损坏武器装备、军事设施、军事通信", "敲诈勒索", "职务侵占"
                ]

    @staticmethod
    def __get_articles_labels():
        return [184, 336, 314, 351, 224, 132, 158, 128, 223, 308, 341, 349, 382, 238, 369, 248, 266, 313, 127, 340, 288,
                172, 209, 243, 302, 200, 227, 155, 147, 143, 261, 124, 359, 343, 291, 241, 235, 367, 393, 274, 240, 269,
                199, 119, 246, 282, 133, 177, 170, 310, 364, 201, 312, 244, 357, 233, 236, 264, 225, 234, 328, 417, 151,
                135, 136, 348, 217, 168, 134, 237, 262, 150, 114, 196, 303, 191, 392, 226, 267, 272, 212, 353, 315, 205,
                372, 215, 350, 275, 385, 164, 338, 292, 159, 162, 333, 388, 356, 375, 326, 402, 397, 125, 395, 290, 176,
                354, 185, 141, 279, 399, 192, 383, 307, 295, 361, 286, 404, 390, 294, 115, 344, 268, 171, 117, 273, 193,
                418, 220, 198, 231, 386, 363, 346, 210, 270, 144, 347, 280, 281, 118, 122, 116, 360, 239, 228, 305, 130,
                152, 389, 276, 213, 186, 413, 285, 316, 245, 232, 175, 149, 263, 387, 283, 391, 211, 396, 352, 345, 258,
                253, 163, 140, 293, 194, 342, 161, 358, 271, 156, 260, 384, 153, 277, 214]

    @staticmethod
    def __get_highlight_ids(attentions, threshold=0.01):  # FIXME 调整阈值
        """
        获取高亮句子下标
        :param attentions: BERT输出的12层注意力
        :param threshold: 阈值
        :return: 高亮字下标位置列表
        """
        attentions = list(attentions)
        attentions = [att.detach().numpy() for att in attentions]
        consider_layers_ids = [7, 10]  # FIXME 0-11共12层，调整考虑的神经层下标数以调整高亮部分的位置
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

    @staticmethod
    def __get_charge_label_ids(preds, threshold=-0.6):  # FIXME 调整阈值
        """
        获取罪名标签下标
        :param preds: 预测结果
        :param threshold: 阈值
        :return: 罪名标签下标列表
        """
        preds = preds.view(-1)
        preds_max = preds.max()
        preds_threshold = preds_max * threshold
        return list(np.where(preds > preds_threshold)[0])

    @staticmethod
    def __predict_charge_and_highlight_ids(model_version, sentence, charge_labels_threshold=-0.6,
                                           highlight_threshold=0.01):
        """
        预测罪名与高亮位置下标
        :param model_version: 模型版本或位置
        :param sentence: 需预测的句子字符串
        :param charge_labels_threshold: 预测罪名标签时的阈值
        :param highlight_threshold: 预测高亮位置时的阈值
        :return: 预测罪名标签下标与高亮位置下标
        """
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

        preds_charge_labels_ids = Predict.__get_charge_label_ids(preds=preds, threshold=charge_labels_threshold)
        preds_highlight_ids = Predict.__get_highlight_ids(attentions=attentions, threshold=highlight_threshold)

        return preds_charge_labels_ids, preds_highlight_ids

    @staticmethod
    def predict_charge_and_highlight(sentence, config=None):

        """
        预测罪名与高亮语句
        :param sentence: 需预测的语句
        :param config: 配置信息，包含 label_type/highlight_label_type: div或text等，用于<div>或<text>； label_cls/highlight_cls: pred-text等。
        :return: 罪名标签列表，高亮后的语句
        """
        if config is None:
            config = dict()
        config_keys = list(config.keys())
        default_config = {"label_type": "text",
                          "label_cls": "pred-text",
                          "highlight_cls": "pred-text-highlight",
                          "highlight_label_type": "text",
                          "model": r"./torch_pretrained_bert_multi_label/tmp/self/",
                          "labels_threshold": -0.6,
                          "highlight_threshold": 0.01}
        config = {key: default_config[key] if (key not in config_keys) else config[key] for
                  key in default_config}
        label_ids, highlight_ids = Predict.__predict_charge_and_highlight_ids(model_version=config["model"],
                                                                              sentence=sentence,
                                                                              charge_labels_threshold=config[
                                                                                  "labels_threshold"],
                                                                              highlight_threshold=config[
                                                                                  "highlight_threshold"])
        label_list = Predict.__get_charge_labels()
        labels = [label_list[ids] for ids in label_ids]
        highlight_sentence_format = "<%s class='{highlight_cls}'>{word}</%s>" % (
            config["highlight_label_type"],
            config["highlight_label_type"])
        highlight_sentence = "".join(
            [highlight_sentence_format.format(
                **{"highlight_cls": config["highlight_cls"],
                   "word": word})
             if i in highlight_ids else word for i, word in enumerate(sentence)])
        sentence = "%s%s%s" % (r"<%s class='%s'>" %
                               (config["label_type"],
                                config["label_cls"]),
                               highlight_sentence,
                               r"</%s>" % config["label_type"])
        need_eliminate = u"</%s><%s class='%s'>" % (
            config["highlight_label_type"], config["highlight_label_type"], config["highlight_cls"])
        sentence = re.sub(need_eliminate, u"", sentence)
        return labels, sentence

    @staticmethod
    def predict_articles(charges, model, labels_threshold):
        articles = [123]
        article_list = Predict().__get_articles_labels()
        # TODO 根据预测的罪名，使用模型，预测法条
        return articles


if __name__ == '__main__':
    # sentence = u"被告人周某在越野车内窃得黑色手机。祁阳县人民检察院指控，2013年9月22日、25日，被告人李某在祁阳县潘市镇石峡洲村，因怀疑别人在谩骂自己，便手持木棍、刀等凶器冲出屋外，追逐本村无辜村民，随意殴打他人，致多人受伤，任意损毁他人财物。经鉴定，被害人李某甲的损伤构成重伤；被害人李某乙、李某丙的损伤均构成了轻伤；被害人李某丁、李某戊、李某己、李某庚、李某辛、黄某某、李某壬、李某癸的损伤均构成轻微伤。2013年9月25日12时许，祁阳县公安局民警将被告人李某抓获归案。该院就上述指控，向本院提供了被害人李某甲、李某乙、李某丙等人的陈述；证人王某甲、王某乙、于某某等人的证言；法医鉴定意见书及伤情照片；现场勘验检查笔录、现场方位图及照片、提取笔录及扣押物品清单、指认木棒和刀照片；公安机关证明；户籍证明及被告人李某供述等相关证据予以证明。该院以被告人李某××他人身体，致一人重伤；同时持凶器追逐、殴打他人，致二人轻伤，多人轻微伤，情节恶劣；任意损毁他人财物，造成恶劣社会影响，情节严重。"
    # labels, highlight_sentence = Predict().predict_charge_and_highlight(sentence=sentence,
    #                                                                     config={"label_type": "div",
    #                                                                             "label_cls": "pred-text",
    #                                                                             "highlight_cls": "pred-text-highlight",
    #                                                                             "highlight_label_type": "div",
    #                                                                             "model": r"/model/torch_pretrained_bert_multi_label/tmp/self/",
    #                                                                             "labels_threshold": -0.6,
    #                                                                             "highlight_threshold": 0.01})
    # print("*" * 10 + " labels " + "*" * 10)
    # print(labels)
    # print("*" * 10 + " sentence " + "*" * 10)
    # print(highlight_sentence)

    charge_labels = ['寻衅滋事', '故意伤害']
