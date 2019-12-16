import os

from py2neo import Graph, NodeMatcher
from tqdm import tqdm

from utils import MultiThread


class DB(object):
    graph = None

    def __new__(cls, config):
        cls.graph = Graph(config["url"], username=config["username"], password=config["password"])
        return None

    @classmethod
    def __search_single_keyword(cls, keyword):
        matcher = NodeMatcher(cls.graph)
        title_nodes = list(matcher.match("标题").where("_.content CONTAINS '%s'" % keyword))
        content_nodes = list(matcher.match("内容").where("_.content CONTAINS '%s'" % keyword))

        def merge_title_content(title, content):
            # TODO 合并content与title的检索结果
            return title, content

        return merge_title_content(title_nodes, content_nodes)

    @classmethod
    def search(cls, keywords):
        threads = []
        keywords_result = list()
        for keyword in tqdm(keywords, desc="CREATE KEYWORDS THREADS"):
            keyword_thread = MultiThread(DB.__search_single_keyword, args=(keyword,))
            keyword_thread.start()
            threads.append(keyword_thread)
        for single_thread in tqdm(threads, desc="ENDING KEYWORDS THREADS"):
            single_thread.join()
            single_result = single_thread.get_result()
            if len(single_result) > 0:
                keywords_result.append(single_result)
        return keywords_result
