# -*- coding: utf-8 -*-
import json
import logging

import requests
from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

from utils import MultiThread
from utils.data.crawler import get_similar_cases
from utils.data.handleq import HandleQ
from utils.engine.db import DB
from utils.model.predict import Predict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info('***** Initializing *****')

with open("config.json", "r") as f:
    configs = json.load(f)

# initialize classes
Predict(configs["PREDICT"]["SMART_EVALUATION"])  # init Predict class
DB(configs["NEO4J"])  # init Database class
HandleQ(configs["HANDLEQ"])  # init HandleQ with baidu

# initialize global variables
CASE_TYPES = configs["CASE_TYPES"]
HTTP_CODE_MESSAGE = configs["HTTP_CODE_MESSAGE"]
app = Flask(__name__)

logger.info('***** End of initialization *****')


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/search')
def search():
    logger.info('***** Search *****')
    q = request.args.get('q')
    ask = request.args.get('ask')
    logger.info(' Question: %s' % q)
    logger.info(' Ask: %s' % ask)
    assert len(q) <= 200
    assert ask in ('html', 'json')
    handle_q = HandleQ(q)
    # handle_q的lcut_correct_q的关键词为其在数据库中搜索到的关键词
    handle_q.keywords_of_lcut_correct_q = DB.search_keywords(handle_q.lcut_correct_q)
    # keywords为handle_q的关键词
    keywords = handle_q.keywords
    # final_q为handle_q中的最终的纠错后替换同义词后的q
    final_q = handle_q.final_q
    # 多线程
    threads = []
    # 在数据库中查找相关法条（多线程）
    articles_thread = MultiThread(DB.search_items, args=(keywords,))
    articles_thread.start()
    threads.append(articles_thread)
    # 从觅律搜索中爬去关键词相关的案例（多线程）
    similar_cases_thread = MultiThread(get_similar_cases, args=(keywords,))
    similar_cases_thread.start()
    threads.append(similar_cases_thread)
    # 预测案情
    prediction = Predict.predict(final_q)
    highlight_key = "重点"
    if highlight_key in list(prediction.keys()):
        handle_q.final_q_highlight = prediction[highlight_key]  # final_q中的高亮词汇，需转换为原始q的高亮词汇
    prediction[highlight_key] = handle_q.highlight  # 修改prediction中的高亮词汇为
    # 多线程结束
    _ = [thread.join() for thread in threads]
    result = {
        "sentence": q,
        "predictions": [{"title": key, "content": prediction[key]} for key in prediction],
        "articles": articles_thread.get_result(),
        "similarCases": similar_cases_thread.get_result(),
    }
    logger.info('***** End of search *****')
    return render_template('search.html', result=result) if ask == 'html' else result


@app.route("/case")
def case():
    uniqid = request.args.get('uniqid')
    case_type = request.args.get('type')
    ask = request.args.get('ask')
    assert case_type in ("authcase", "case")
    assert ask in ('html', 'json')
    url = "https://solegal.cn/api/v2/%s/detail?uniqid=%s" % (case_type, uniqid)
    case_raw = requests.get(url=url).json()["data"]
    case_detail = {
        "title": case_raw["TITLE"],
        "baseList": case_raw["baseList"],
        "contents": [{'title': c["title"], "strContent": c["strContent"].split('\n')} for c in case_raw["contents"]]
    }
    return render_template("case.html", case_detail=case_detail) if ask == 'html' else case_detail


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


if __name__ == '__main__':
    # keywords = ["抢劫", "盗窃"]
    # start_time = time()
    # print("-" * 20 + ' articles ' + "-" * 20)
    # print(DB.search_items(keywords=keywords))
    # print("cost time: %.02f" % (time() - start_time))

    # synonyms = ["募", "生", "维系"]
    # start_time = time()
    # print(DB.search_keywords(synonyms=synonyms))
    # print("cost time: %.02f" % (time() - start_time))

    q = u"偷东西"
    handle_q = HandleQ(q)
    print(handle_q.correct_q)

    # handle_q的lcut_correct_q的关键词为其在数据库中搜索到的关键词
    handle_q.keywords_of_lcut_correct_q = DB.search_keywords(handle_q.lcut_correct_q)
    for i in range(len(handle_q.lcut_correct_q)):
        print(i, handle_q.lcut_correct_q[i], handle_q.keywords_of_lcut_correct_q[i])
#     # keywords为handle_q的关键词
#     keywords = handle_q.keywords
#     # final_q为handle_q中的最终的纠错后替换同义词后的q
#     final_q = handle_q.final_q
#     # 多线程
#     threads = []
#     # 在数据库中查找相关法条（多线程）
#     articles_thread = MultiThread(DB.search_items, args=(keywords,))
#     threads.append(articles_thread)
#     # 从觅律搜索中爬去关键词相关的案例（多线程）
#     similar_cases_thread = MultiThread(get_similar_cases, args=(keywords,))
#     threads.append(similar_cases_thread)
#     # 多线程开始
#     _ = [thread.start() for thread in threads]
#     # 预测案情
#     prediction = Predict.predict(final_q)
#     highlight_key = "重点"
#     if highlight_key in list(prediction.keys()):
#         handle_q.final_q_highlight = prediction[highlight_key]  # final_q中的高亮词汇，需转换为原始q的高亮词汇
#     prediction[highlight_key] = handle_q.highlight  # 修改prediction中的高亮词汇为
#     # 多线程结束
#     _ = [thread.join() for thread in threads]
#     # result = {
#     #     "sentence": q,
#     #     "predictions": [
#     #         {
#     #             "title": "种类",
#     #             "content": ['刑事案由']
#     #         }, {
#     #             "title": "罪名",
#     #             "content": ["抢劫", "盗窃"],
#     #         }, {
#     #             "title": "高亮",
#     #             "content": ['抢', '手机']
#     #         }, {
#     #             "title": "法条",
#     #             "content": [20, 30]
#     #         }, {
#     #             "title": "监禁",
#     #             "content": ['短期 (≤3)']
#     #         }
#     #     ],
#     #     "articles": [
#     #         {
#     #             "title": ["第一条", "立法宗旨"],
#     #             "source": ["刑法", "第一编", "第一章"],
#     #             "content": "为了惩罚犯罪，保护人民，根据宪法，结合我国同犯罪作斗争的具体经验及实际情况，制定本法。"
#     #         },
#     #         {
#     #             "title": ["第二条", "本法任务"],
#     #             "source": ["刑法", "第一编", "第一章"],
#     #             "content": "中华人民共和国刑法的任务，是用刑罚同一切犯罪行为作斗争，以保卫国家安全，"
#     #                        "保卫人民民主专政的政权和社会主义制度，保护国有财产和劳动群众集体所有的财产，"
#     #                        "保护公民私人所有的财产，保护公民的人身权利、民主权利和其他权利，维护社会秩序、"
#     #                        "经济秩序，保障社会主义建设事业的顺利进行。"
#     #         },
#     #         {
#     #             "title": ["第三条", "罪刑法定"],
#     #             "source": ["刑法", "第一编", "第一章"],
#     #             "content": "法律明文规定为犯罪行为的，依照法律定罪处刑；法律没有明文规定为犯罪行为的，不得定罪处刑。"
#     #         }
#     #     ],
#     #     "similarCases": {
#     #         "authcase": [
#     #             {
#     #                 "uniqid": "f02b1fc6-e8ad-4730-a26a-f7a94ef34f8b",
#     #                 "title": "重庆市渝中区人民检察院诉朱波伟、雷秀平抢劫案",
#     #                 "baseList": ["《最高人民法院公报》  2006年第4期(总:114期)", "重庆市渝中区人民法院"]
#     #             },
#     #             {
#     #                 "uniqid": "1c0337d0-51d3-45ff-a389-cfbca11a3fca",
#     #                 "title": "检例第23号：蔡金星、陈国辉等（抢劫）不核准追诉案",
#     #                 "baseList": ["最高人民检察院"]
#     #             }
#     #         ],
#     #         "case": [
#     #             {
#     #                 "uniqid": "7baf7d60-a40f-4d4a-800d-c5a7758d507e",
#     #                 "title": "常斌抢劫罪、寻衅滋事罪刑罚与执行变更刑事裁定书",
#     #                 "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更558号", "2018-02-01"]
#     #             },
#     #             {
#     #                 "uniqid": "50c7c56b-4419-4b79-8cac-83f9dd33db9e",
#     #                 "title": "武俊肥故意杀人罪、抢劫罪等刑罚与执行变更刑事裁定书",
#     #                 "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更607号", "2018-02-01"]
#     #             }
#     #
#     #         ]
#     #     },
#     #
#     # }
#     result = {
#         "sentence": q,
#         "predictions": [{"title": key, "content": prediction[key]} for key in prediction],
#         "articles": articles_thread.get_result(),
#         "similarCases": similar_cases_thread.get_result(),
#     }
#     print(result)
