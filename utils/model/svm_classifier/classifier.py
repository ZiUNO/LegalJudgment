import csv
import re
import sys
from datetime import datetime

import joblib
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC


class SVMClassifier(object):
    clf = None
    save_path = None

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
    def convert_charge_to_ids(charges):
        charge_list = SVMClassifier.__get_charge_labels()
        charge_len = len(charge_list)
        charge_ids = [0] * charge_len
        for ch in charges:
            charge_ids[charge_list.index(ch)] = 1
        return charge_ids

    @staticmethod
    def convert_ids_to_charge(ids):
        charge_list = SVMClassifier.__get_charge_labels()
        charge_ids = list(np.where(ids)[0])
        return [charge_list[index] for index in charge_ids]

    @staticmethod
    def convert_ids_to_article(ids):
        article_list = SVMClassifier.__get_articles_labels()
        article_ids = list(np.where(ids)[0])
        return [article_list[index] for index in article_ids]

    @staticmethod
    def convert_article_to_ids(articles):
        article_list = SVMClassifier.__get_articles_labels()
        article_len = len(article_list)
        article_ids = [0] * article_len
        for ar in articles:
            article_ids[article_list.index(ar)] = 1
        return article_ids

    @staticmethod
    def tsv2dataset(tsv):
        datasets = {"X": [], "y": []}
        for i, line in enumerate(tsv):
            if i == 0:
                continue
            article = line[1][1:-1].split(',')
            article = list(set([int(i.strip()) for i in article]))
            article_ids = SVMClassifier.convert_article_to_ids(articles=article)
            charge = list(set(re.findall(u"'(.*?)'", line[2], re.S)))
            charge_ids = SVMClassifier.convert_charge_to_ids(charges=charge)
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
