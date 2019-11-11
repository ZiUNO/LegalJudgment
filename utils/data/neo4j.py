import json
import os

import jieba
import numpy as np
from py2neo import Graph, Node, Relationship, NodeMatcher
from sklearn.feature_extraction.text import TfidfVectorizer


class Neo4j(object):
    """
    对整个文件夹进行创建数据库
    """
    stopwords = None

    def __init__(self, dir_name, rebuild=False):
        self.__rebuild = rebuild
        root = Node('文件夹', name=dir_name)
        self.__dir_name = dir_name

        self.__graph = Graph('http://192.168.140.61:7474', username='ziuno', password='1234')  # ip需更改为服务器的地址

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
        with open(os.path.join(os.getcwd(), 'utils', '中文停用词表.txt'), 'r', encoding='utf-8') as f:
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

        selector = NodeMatcher(self.__graph)
        titles = list(selector.match('标题'))
        titles = {title['title']: title for title in titles}
        contents = list(selector.match('内容'))
        contents = {content['content']: content for content in contents}

        def get_voca_vec_node(item):
            keys = list(item.keys())
            nodes = [item[key] for key in keys]
            keys = [' '.join(jieba.cut(key)) for key in keys]
            tf_idf = TfidfVectorizer(stop_words=Neo4j.stopwords)
            vectors = tf_idf.fit_transform(keys).toarray()
            vocabulary = tf_idf.vocabulary_
            return vocabulary, vectors, nodes

        self.__titles_vocabulary, self.__titles_vectors, self.__titles_nodes = get_voca_vec_node(titles)
        self.__content_vocabulary, self.__content_vectors, self.__content_nodes = get_voca_vec_node(contents)
        # vectors和nodes中的下标相对应
        print("SUCCESSFULLY EXPAND %s" % law)

    def expand(self, laws='ALL'):
        """
        展开指定法律（仅支持到各个条目级别的显示）
        :param laws: law（str类型）或laws（list类型，其中包含多个str）
        :return:
        """
        laws = self.__laws.keys() if laws == 'ALL' else laws
        laws = [laws] if isinstance(laws, str) else laws
        for law in laws:
            self.__expand_law(law)

    def answer(self, question):
        print('SEARCHING...')
        question = ' '.join(jieba.cut(question, cut_all=True))
        tf_idf_title = TfidfVectorizer(vocabulary=self.__titles_vocabulary, stop_words=Neo4j.stopwords)
        tf_idf_content = TfidfVectorizer(vocabulary=self.__content_vocabulary, stop_words=Neo4j.stopwords)
        que_vec_title = tf_idf_title.fit_transform([question]).toarray()[0]
        que_vec_content = tf_idf_content.fit_transform([question]).toarray()[0]

        def distance(vec, matrix):
            vector_mat = np.mat(vec)
            matrix_mat = np.mat(matrix)
            num = matrix_mat * vector_mat.T
            den = np.linalg.norm(vector_mat) * np.linalg.norm(matrix_mat, axis=1, keepdims=True)
            # print(np.sum(num), np.sum(den))
            sim = 0.5 + (0.5 * num) / den
            return np.ravel(sim)

        que_title_dis = distance(que_vec_title, self.__titles_vectors)
        que_content_dis = distance(que_vec_content, self.__content_vectors)
        max_title_index = int(np.argmax(que_title_dis))
        max_content_index = int(np.argmax(que_content_dis))
        title_node = self.__titles_nodes[max_title_index]
        content_node = self.__content_nodes[max_content_index]
        result = [list(title_node.values())[0], list(content_node.values())[0]]
        # TODO 向文件方向检索当前所在条并加入到结果result中
        return result


class Neo4jLaw(object):
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            law = json.load(f)
        self.__graph = Graph('http://localhost:7474', username='ziuno', password='1234')
        self.__law = law
