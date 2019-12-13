# -*- coding: utf-8 -*-
import json
from threading import Thread

from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from utils.model.predict import Predict


class MultiThread(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.__func = func
        self.__args = args
        self.__result = None

    def run(self):
        self.__result = self.__func(*self.__args)

    def get_prediction(self):
        return self.__result


with open("config.json", "r") as f:
    configs = json.load(f)

Predict(configs["SMART_EVALUATION"])
CASE_TYPES = configs["CASE_TYPES"]
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search')
def search():
    q = request.args.get('q')
    # TODO q纠正错别字->correct_q
    correct_q = q
    # TODO correct_q同义词替换并获取关键词->final_q, keywords
    final_q = correct_q
    # FROM HERE 根据final_q获得最终结果
    # TODO 检索获得来自数据库的法条
    db_items = []
    # TODO 根据关键词获取相关案例
    similar_cases = []
    # TODO 根据final_q预测案件种类case_type_id
    case_type_id = 0
    case_type = CASE_TYPES[case_type_id]
    result = {
        "db_items": db_items,
        "similar_cases": similar_cases,
        "case_type": case_type
    }
    # 当案件种类为"刑事案件"时，预测罪名、高亮位置、法条
    if case_type == "刑事案件":
        pred_charge_labels, highlight_sentence = \
            Predict.predict_charge_and_highlight(final_q,
                                                 {"label_type": "text",
                                                  "label_cls": "pred-text",
                                                  "highlight_cls": "pred-text-highlight",
                                                  "highlight_label_type": "div"})
        articles = Predict.predict_articles(pred_charge_labels)
        # TODO 汇总结果
        result["pred"] = {"pred_charge_labels": pred_charge_labels,
                          "highlight_sentence": highlight_sentence,
                          "articles": articles}
    # TO HERE
    result = json.dumps(result)
    return result


@app.route('/search/case')
def case():
    # TODO 爬去觅律经过并返回
    return None


@app.errorhandler(HTTPException)
def handle_exception(e):
    exception = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    return render_template("exception.html", exception=exception)
