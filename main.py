import json
import os
import platform
import sys

from utils.engine.neo4j_engine import Neo4j

if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        config = json.load(f)
    law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=True)
    graph.expand('中华人民共和国刑法')
    say = input('>>>')
    while say != 'q':
        ans = graph.answer(say)  # 抢劫罪是什么？
        for a in ans:
            print(a)
        say = input('>>>')
