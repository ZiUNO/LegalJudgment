# -*- coding: utf-8 -*-
import json
import os

from tqdm import tqdm

from utils import MultiThread
from utils.data.crawler import get_synonyms
from utils.engine.neo4j_engine import Neo4j


def rebuild_graph():
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path)
    graph.expand()
    with open(os.path.join('data', 'synonyms.json'), 'r', encoding='utf-8') as f:
        synonyms = json.load(f)
    print(synonyms)
    # 在数据库中保存同义词
    graph.save_synonyms(synonyms=synonyms)


def get_keywords():
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=False)
    return graph.keywords()


def download_synonyms(keywords):
    # single thread
    with open(os.path.join('data', 'synonyms.json'), 'r', encoding='utf-8') as f:
        has_download_synonyms = json.load(f)
    has_download_keywords = list(has_download_synonyms.keys())

    with open(os.path.join('data', 'keywords.json'), 'r', encoding='utf-8') as f:
        keywords_config = json.load(f)

    ignore_keywords = keywords_config['ignore']
    fail_to_download_keywords = keywords_config['fail_to_download']
    consider_keywords = keywords_config["consider"]

    not_download_keywords = list(set(keywords).union(set(consider_keywords))
                                 - set(has_download_keywords) - set(fail_to_download_keywords) - set(ignore_keywords))

    # # FROMHERE
    # print("-" * 50)
    # print("Need to download:")
    # tmp = str(sorted(not_download_keywords)).replace("'", '"')
    # input(tmp)
    # print("-" * 50)
    # print("Before download fail_to_download:")
    # print(keywords_config["fail_to_download"])
    # # TOHERE

    synonyms = get_synonyms(not_download_keywords)
    for s in synonyms:
        if len(synonyms[s]) == 1 and synonyms[s][0] == s:
            keywords_config["fail_to_download"].append(s)

    # # FROMHERE
    # print("-" * 50)
    # print("After download fail_to_download:")
    # print(keywords_config["fail_to_download"])
    # # TOHERE

    keywords_config["fail_to_download"] = list(set(keywords_config["fail_to_download"]))

    keywords_config["successful_download"] = list(synonyms.keys())
    with open(os.path.join('data', 'keywords.json'), 'w') as f:
        json.dump(keywords_config, f, ensure_ascii=False, indent=2)

    synonyms.update(has_download_synonyms)
    for i in ignore_keywords:
        try:
            del synonyms[i]
        except KeyError:
            continue
    with open(os.path.join('data', 'synonyms.json'), 'w') as f:
        json.dump(synonyms, f, ensure_ascii=False, indent=2)


# NOTE:执行步骤：crawler.py->transform.py->main.py->flask run.py
if __name__ == '__main__':
    keywords = get_keywords()  # 获取数据库中的关键词
    # print(keywords)
    download_synonyms(keywords=keywords)  # 重新下载同义词
    rebuild_graph()  # 重建数据库
    pass
