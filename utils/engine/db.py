import logging
import re

from py2neo import Graph
from tqdm import tqdm

from utils import MultiThread, merge

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DB(object):
    graph = None

    def __new__(cls, config):
        cls.graph = Graph(config["url"], username=config["username"], password=config["password"])
        return None

    @classmethod
    def __search_item(cls, keyword):
        nodes = list(cls.graph.run(
            "MATCH(label:标签)-->(content:内容) "
            "MATCH(label)-->(title:标题) "
            "WHERE "
            "content.content CONTAINS '%s' "
            "OR "
            "title.title CONTAINS '%s' "
            "MATCH path=(file:文件)-[*]->(label) "
            "RETURN path, title, content" % (keyword, keyword)
        ))
        nodes = [{"path": node["path"],
                  "title": node["title"],
                  "content": node["content"]}
                 for node in nodes]
        item = []
        for node in nodes:
            path = node["path"].nodes
            file_name = path[0]["name"]
            piece_label_name = re.sub(u"\s*", "", path[1]["label"])
            chapter_label_name = path[3]["label"]
            item_label_name = path[5]["label"]
            source = [file_name.replace("中华人民共和国", ""), piece_label_name, chapter_label_name]
            source = [s for s in source if s != '']
            content = re.split(r'\n|</br>', node["content"]["content"])
            item.append({"title": [item_label_name, node["title"]["title"]],
                         "source": source,
                         "content": content})
        return item

    @classmethod
    def __search_keyword(cls, synonym):
        nodes = list(cls.graph.run(
            "MATCH(keyword:关键词)-->(synonym:同义词) "
            "WHERE synonym.synonym = '%s' "  # FIXME CONTAINS可能修改为 =
            "RETURN keyword.keyword" % synonym
        ))
        if len(nodes) == 0:
            return None
        keyword = nodes[0][0]
        return keyword

    @classmethod
    def search_items(cls, keywords):
        threads = []
        items_result = list()
        tmp_key = "items"
        logger.info('***** Search items *****')
        for keyword in tqdm(keywords, desc='Create items threads'):
            keyword_thread = MultiThread(DB.__search_item, args=(keyword,))
            keyword_thread.start()
            threads.append(keyword_thread)
        for single_thread in tqdm(threads, desc="End items threads"):
            single_thread.join()
            single_result = single_thread.get_result()
            items_result.append({tmp_key: single_result})
        items_result = merge(items_result)[tmp_key]
        return items_result

    @classmethod
    def search_keywords(cls, synonyms):
        threads = []
        keywords_result = list()
        logger.info('***** Search keywords *****')
        for synonym in tqdm(synonyms, desc="Create keywords threads"):
            synonym_thread = MultiThread(DB.__search_keyword, args=(synonym,))
            synonym_thread.start()
            threads.append(synonym_thread)
        for single_thread in tqdm(threads, desc="End keywords threads"):
            single_thread.join()
            single_result = single_thread.get_result()
            keywords_result.append(single_result)
        return keywords_result
