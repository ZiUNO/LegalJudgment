import sys

from utils.neo4j import Neo4j

if __name__ == '__main__':
    # DuXiaoFaCrawler.download(sys.argv[1])  # 法律条文爬取

    graph = Neo4j(sys.argv[1])
