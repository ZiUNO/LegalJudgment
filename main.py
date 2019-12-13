# -*- coding: utf-8 -*-
import json
import os

from utils.engine.neo4j_engine import Neo4j

if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=True)
    graph.expand()

