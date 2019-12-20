# -*- coding: utf-8 -*-
import json
import os

from tqdm import tqdm

from utils import MultiThread
from utils.data.crawler import get_synonyms
from utils.engine.neo4j_engine import Neo4j

# NOTE:执行步骤：crawler.py->transform.py->main.py
if __name__ == '__main__':
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=False)
    # graph.expand()
    keywords = graph.keywords(1)

    # test 100
    # print(keywords)
    keywords = set(list(keywords)[:100])

    # single thread
    print(get_synonyms(keywords))

    # multi threads
    # threads = []
    # for word in tqdm(words, "CREATING THREAD"):
    #     thread = MultiThread(get_synonyms, args=(word, ))
    #     thread.start()
    #     threads.append(thread)
    # _ = [thread.join() for thread in threads]
    # results = {}
    # _ = [results.update(thread.get_result()) for thread in threads]
    # print(results)

    # result = [{"title": "a", "content": "b"}, {"title": "a", "content": "b"}, {"title": "c", "content": "d"}]
    # merged_result = merge(result)
    # print(merged_result)
