import sys

from utils.crawler import DuXiaoFaCrawler
from utils.neo4j import Neo4j

if __name__ == '__main__':
    if 1:  # 自行更改是否进行爬取
        DuXiaoFaCrawler.download(sys.argv[1])

    # graph = Neo4j(sys.argv[1])
