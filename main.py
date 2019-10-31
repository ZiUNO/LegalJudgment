# import json
# import sys
#
# from utils import transform
# from utils.crawler import DuXiaoFaCrawler
# from utils.neo4j import Neo4j


def save_to_txt(txt, path):
    with open(path, 'w') as f:
        f.write('\n'.join(txt))


if __name__ == '__main__':
    # config_path = sys.argv[1]
    # DuXiaoFaCrawler.download(config_path)  # 法律条文爬取
    # with open(config_path, 'r', encoding='utf-8') as f:
    #     config = json.load(f)
    # dxf_path = config['DOWNLOAD_SAVE_PATH']
    # law_path = config['LAW_PATH']  # 格式化后的法律条文的保存路径
    # transform.to_law(dxf_path, law_path)  # 格式化下载的法律条文
    # graph = Neo4j(law_path)
    # graph.expand('中华人民共和国刑法')
    # leaves = graph.leaves()
    # save_to_txt(leaves, '刑法.txt')
    # TODO 分析刑法.txt
    pass
