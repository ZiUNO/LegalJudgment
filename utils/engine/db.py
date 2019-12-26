import os
import re

from py2neo import Graph, NodeMatcher
from tqdm import tqdm

from utils import MultiThread, merge


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
        print(nodes)
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
            item.append({"title": [item_label_name, node["title"]["title"]],
                         "source": source,
                         "content": node["content"]["content"].split('\n')})
        return item

    @classmethod
    def __search_keyword(cls, synonym):
        # TODO - 2 依据数据库实现搜索同义词的关键词 (若不存在关键词则返回None）
        keyword = synonym
        return keyword

    @classmethod
    def search_items(cls, keywords):
        threads = []
        items_result = list()
        tmp_key = "items"
        for keyword in tqdm(keywords, desc="CREATE ITEMS THREADS"):
            keyword_thread = MultiThread(DB.__search_item, args=(keyword,))
            keyword_thread.start()
            threads.append(keyword_thread)
        for single_thread in tqdm(threads, desc="ENDING ITEMS THREADS"):
            single_thread.join()
            single_result = single_thread.get_result()
            items_result.append({tmp_key: single_result})
        items_result = merge(items_result)[tmp_key]
        # items_result = [
        #     {
        #         "title": ["第一条", "立法宗旨"],
        #         "source": ["刑法", "第一编", "第一章"],
        #         "content": "为了惩罚犯罪，保护人民，根据宪法，结合我国同犯罪作斗争的具体经验及实际情况，制定本法。"
        #     },
        #     {
        #         "title": ["第二条", "本法任务"],
        #         "source": ["刑法", "第一编", "第一章"],
        #         "content": "中华人民共和国刑法的任务，是用刑罚同一切犯罪行为作斗争，以保卫国家安全，"
        #                    "保卫人民民主专政的政权和社会主义制度，保护国有财产和劳动群众集体所有的财产，"
        #                    "保护公民私人所有的财产，保护公民的人身权利、民主权利和其他权利，维护社会秩序、"
        #                    "经济秩序，保障社会主义建设事业的顺利进行。"
        #     },
        #     {
        #         "title": ["第三条", "罪刑法定"],
        #         "source": ["刑法", "第一编", "第一章"],
        #         "content": "法律明文规定为犯罪行为的，依照法律定罪处刑；法律没有明文规定为犯罪行为的，不得定罪处刑。"
        #     }
        # ]
        return items_result

    @classmethod
    def search_keywords(cls, synonyms):
        threads = []
        keywords_result = list()
        for synonym in tqdm(synonyms, desc="[db]-[search_keywords]-CREATE KEYWORDS THREADS"):
            synonym_thread = MultiThread(DB.__search_keyword, args=(synonym,))
            synonym_thread.start()
            threads.append(synonym_thread)
        for single_thread in tqdm(threads, desc="[db]-[search_keywords]-ENDING KEYWORDS THREADS"):
            single_thread.join()
            single_result = single_thread.get_result()
            keywords_result.append(single_result)
        return keywords_result
