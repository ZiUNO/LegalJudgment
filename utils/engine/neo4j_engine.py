import json
import os

import jieba
import jieba.analyse
import numpy as np
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm


class Neo4j(object):
    """
    对整个文件夹进行创建数据库
    """
    stopwords = None

    def __init__(self, dir_name, rebuild=True):
        self.__rebuild = rebuild
        root = Node('文件夹', name=dir_name.split('/')[-1])
        self.__dir_name = dir_name

        # self.__graph = Graph('http://192.168.140.61:7474', username='ziuno', password='1234')  # ip需更改为服务器的地址
        self.__graph = Graph('http://localhost:7474', username='ziuno', password='1234')
        self.__laws = {}
        if rebuild:
            self.__graph.delete_all()
            self.__graph.create(root)
            for dirs in os.listdir(dir_name):
                if dirs.startswith('.'):
                    continue
                text = dirs
                son = Node('文件夹', name=text)
                belong = Relationship(root, '包含', son)
                self.__graph.create(belong)
                for txt in os.listdir(os.path.join(dir_name, dirs)):
                    text = txt.split('.')[0]
                    grandson = Node('文件', name=text)
                    self.__laws[text] = {'node': grandson, 'path': os.path.join(dir_name, dirs, txt)}
                    belong = Relationship(son, '包含', grandson)
                    self.__graph.create(belong)
        else:
            def get_law_path(law, dir_name):
                law = law + '.json'
                for root, dirs, files in list(os.walk(dir_name)):
                    if law in files:
                        return os.path.join(root, law)

            selector = NodeMatcher(self.__graph)
            laws = list(selector.match('文件'))
            for law in laws:
                self.__laws[law['name']] = {'node': law, 'path': get_law_path(law['name'], dir_name)}
        with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], '中文停用词表.txt'), 'r', encoding='utf-8') as f:
            stopwords = f.readlines()
        Neo4j.stopwords = set([stopword.strip() for stopword in stopwords])

    def __expand_law(self, law):
        """
        在数据库中展开指定法律名的法律文件
        :param law: 法律名
        """
        if self.__rebuild:
            def get_nodes(graph, item):
                item_title_node = None
                try:
                    item_title = item['title']
                    item_title_node = Node('标题', title=item_title)
                except KeyError:
                    pass
                item_content = item['content']
                if isinstance(item_content, str):
                    item_content_node = Node('内容', content=item_content)
                elif isinstance(item_content, dict):
                    item_content_node = Node('（内容）', content='内容')
                    for chapter in item_content:
                        chapter_node = Node('标签', label=chapter)
                        graph.create(Relationship(item_content_node, '包含', chapter_node))
                        chapter_title_node, chapter_content_node = get_nodes(graph, item_content[chapter])
                        if chapter_title_node is not None:
                            graph.create(Relationship(chapter_node, '标题', chapter_title_node))
                        graph.create(Relationship(chapter_node, '内容', chapter_content_node))
                else:
                    raise RuntimeError("数据类型错误")
                return item_title_node, item_content_node

            law_node = self.__laws[law]['node']
            law_path = self.__laws[law]['path']
            with open(law_path, 'r', encoding='utf-8') as f:
                law_content = json.load(f)
            for piece in law_content:
                piece_node = Node('标签', label=piece)
                self.__graph.create(Relationship(law_node, '包含', piece_node))
                piece_title_node, piece_content_node = get_nodes(self.__graph, law_content[piece])
                if piece_title_node is not None:
                    self.__graph.create(Relationship(piece_node, '标题', piece_title_node))
                self.__graph.create(Relationship(piece_node, '内容', piece_content_node))
        # print("SUCCESSFULLY EXPAND %s" % law)

    def expand(self, laws='ALL'):
        """
        展开指定法律（仅支持到各个条目级别的显示）
        :param laws: law（str类型）或laws（list类型，其中包含多个str）
        :return:
        """
        laws = list(self.__laws.keys()) if laws == 'ALL' else laws
        laws = [laws] if isinstance(laws, str) else laws
        for law in tqdm(laws, desc="EXPANDING LAWS"):
            self.__expand_law(law)

    def keywords(self, title_top_k=100, content_top_k=150):
        file2content = self.__graph.run(
            '''
            MATCH(file:文件)-[*]->(content:内容)
            RETURN file.name, content.content
            '''
        ).data()
        file2title = self.__graph.run(
            '''
            MATCH(file:文件)-[*]->(title:标题)
            RETURN file.name, title.title
            '''
        ).data()
        file = list([file["file.name"] for file in file2content])
        content = {f: [] for f in file}
        title = {f: [] for f in file}
        data = {f: [] for f in file}
        _ = [content[f["file.name"]].append(f["content.content"]) for f in file2content]
        _ = [title[f["file.name"]].append(f["title.title"]) for f in file2title]
        # jieba.analyse.set_stop_words(os.path.join(os.path.split(os.path.realpath(__file__))[0], '中文停用词表.txt'))
        # content = {f: jieba.analyse.extract_tags('\n'.join(content[f]), topK=content_top_k) for f in content}
        # title = {f: jieba.analyse.extract_tags('\n'.join(title[f]), topK=title_top_k) for f in title}
        # print(title)
        # TODO 使用精确分词进行分词，抢劫罪==>抢劫/抢劫罪（抢劫有同义词但抢劫罪没有）
        data = {f: tuple(set(content[f] + title[f])) for f in data}
        return data
