# -*- coding: utf-8 -*-
import json
import os

from tqdm import tqdm

from utils import MultiThread
from utils.data.crawler import get_synonyms
from utils.engine.neo4j_engine import Neo4j

# NOTE:执行步骤：crawler.py->transform.py->main.py->flask run.py
if __name__ == '__main__':
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=True)
    graph.expand()
    # keywords = graph.keywords(50)

    # test 100
    # print(keywords)
    # keywords = set(list(keywords)[:10])

    # single thread
    # synonyms = get_synonyms(keywords)
    # with open(os.path.join('data', 'synonyms.json'), 'w') as f:
    #     json.dump(synonyms, f, ensure_ascii=False)
    with open(os.path.join('data', 'synonyms.json'), 'r', encoding='utf-8') as f:
        synonyms = json.load(f)
    print(synonyms)

    # 在数据库中保存同义词
    graph.save_synonyms(synonyms=synonyms)

    # result = [{"title": "a", "content": "b"}, {"title": "a", "content": "b"}, {"title": "c", "content": "d"}]
    # merged_result = merge(result)
    # print(merged_result)
