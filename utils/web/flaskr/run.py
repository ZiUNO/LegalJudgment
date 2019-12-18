# -*- coding: utf-8 -*-
import json
from threading import Thread
from time import time

from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from utils.model.predict import Predict
from utils.engine.db import DB

with open("config.json", "r") as f:
    configs = json.load(f)

# initialize classes
Predict(configs["PREDICT"]["SMART_EVALUATION"])  # init Predict class
DB(configs["NEO4J"])  # init Database class

# initialize global variables
CASE_TYPES = configs["CASE_TYPES"]
HTTP_CODE_MESSAGE = configs["HTTP_CODE_MESSAGE"]
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search')
def search():
    q = request.args.get('q')
    # # TODO q纠正错别字->correct_q
    # correct_q = q
    # # TODO correct_q同义词替换并获取关键词->final_q, keywords
    # final_q = correct_q
    # keywords = ["抢劫", "盗窃"]
    # # FROM HERE 根据final_q获得最终结果
    # # TODO 检索获得来自数据库的法条
    # db_items = DB.search(keywords=keywords)
    # # TODO 根据关键词获取相关案例
    # similar_cases = []
    # # TODO 根据final_q预测案件种类case_type_id
    # case_type_id = 0
    # case_type = CASE_TYPES[case_type_id]
    # result = {
    #     "db_items": db_items,
    #     "similar_cases": similar_cases,
    #     "case_type": case_type
    # }
    # # 当案件种类为"刑事案件"时，预测罪名、高亮位置、法条
    # if case_type == "刑事案件":
    #     pred_start_time = time()
    #     pred_charge_labels, highlight_sentence = \
    #         Predict.predict_charge_and_highlight(final_q,
    #                                              {"label_type": "text",
    #                                               "label_cls": "pred-text",
    #                                               "highlight_cls": "pred-text-highlight",
    #                                               "highlight_label_type": "div"})
    #     articles = Predict.predict_articles(pred_charge_labels)
    #     # TODO 汇总结果
    #     result["pred"] = {"pred_charge_labels": pred_charge_labels,
    #                       "highlight_sentence": highlight_sentence,
    #                       "articles": articles,
    #                       "pred_cost_time": round(time() - pred_start_time, 2)}
    # TO HERE
    result = {
        "sentence": "抢劫",
        "highlight": [0, 1],
        "predictions": [
            {
                "title": "案情种类",
                "content": ["刑事案件"]
            },
            {
                "title": "罪名",
                "content": ["抢劫", "盗窃"],
            },
            {
                "title": "法条",
                "content": ["20", "30"]
            }
        ],
        "articles": [
            {
                "title": ["第一条", "立法宗旨"],
                "from": ["刑法", "第一编", "第一章"],
                "content": "为了惩罚犯罪，保护人民，根据宪法，结合我国同犯罪作斗争的具体经验及实际情况，制定本法。"
            },
            {
                "title:": ["第二条", "本法任务"],
                "from": ["刑法", "第一编", "第一章"],
                "content": "中华人民共和国刑法的任务，是用刑罚同一切犯罪行为作斗争，以保卫国家安全，"
                           "保卫人民民主专政的政权和社会主义制度，保护国有财产和劳动群众集体所有的财产，"
                           "保护公民私人所有的财产，保护公民的人身权利、民主权利和其他权利，维护社会秩序、"
                           "经济秩序，保障社会主义建设事业的顺利进行。"
            },
            {
                "title": ["第三条", "罪刑法定"],
                "from": ["刑法", "第一编", "第一章"],
                "content": "法律明文规定为犯罪行为的，依照法律定罪处刑；法律没有明文规定为犯罪行为的，不得定罪处刑。"
            }
        ],
        "similarCases": {
            "authcase": [
                {
                    "uniqid": "f02b1fc6-e8ad-4730-a26a-f7a94ef34f8b",
                    "title": "重庆市渝中区人民检察院诉朱波伟、雷秀平抢劫案",
                    "baseList": ["《最高人民法院公报》  2006年第4期(总:114期)", "重庆市渝中区人民法院"]
                },
                {
                    "uniqid": "1c0337d0-51d3-45ff-a389-cfbca11a3fca",
                    "title": "检例第23号：蔡金星、陈国辉等（抢劫）不核准追诉案",
                    "baseList": ["最高人民检察院"]
                }
            ],
            "case": [
                {
                    "uniqid": "7baf7d60-a40f-4d4a-800d-c5a7758d507e",
                    "title": "常斌抢劫罪、寻衅滋事罪刑罚与执行变更刑事裁定书",
                    "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更558号", "2018-02-01"]
                },
                {
                    "uniqid": "50c7c56b-4419-4b79-8cac-83f9dd33db9e",
                    "title": "武俊肥故意杀人罪、抢劫罪等刑罚与执行变更刑事裁定书",
                    "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更607号", "2018-02-01"]
                }

            ]
        },

    }
    return render_template('search.html', result=result)


@app.route('/search/case')
def case():
    # TODO 爬去觅律经过并返回
    return None


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(HTTPException)
def handle_exception(e):
    code = e.code
    message = HTTP_CODE_MESSAGE[str(code)]
    exception = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "message": message
    }
    return render_template("exception.html", exception=exception)
