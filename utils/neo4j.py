import json
import os
import re

from py2neo import Graph, Node, Relationship


class Neo4j(object):
    def __init__(self, dir_name):
        self.__dir_name = dir_name
        self.__graph = Graph('http://localhost:7474', username='ziuno', password='1234')
        self.__graph.delete_all()
        root = Node('文件夹', name=dir_name)
        self.__graph.create(root)
        self.__laws = {}
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

    def __expand_law(self, law):
        """
        在数据库中展开指定法律名的法律文件
        :param law: 法律名
        """

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
                item_content_node = Node('内容', content='内容')
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
        print("SUCCESSFULLY EXPAND %s" % law)

    def expand(self, laws='ALL'):
        """
        展开指定法律
        :param laws: law（str类型）或laws（list类型，其中包含多个str）
        :return:
        """
        laws = self.__laws.keys() if laws == 'ALL' else laws
        laws = [laws] if isinstance(laws, str) else laws
        for law in laws:
            self.__expand_law(law)

    def leaves(self):
        """
        获取所有叶节点的信息
        :return:
        """
        leaves = self.__graph.run("MATCH(n) WHERE not (n)-->() RETURN n").data()
        for i, leaf in enumerate(leaves):
            leaf_value = re.sub(u"^.*: '|'\}\)", "", str(list(leaf.values())[0]))
            leaves[i] = str(leaf_value.encode().decode('unicode_escape'))
        leaves = [leaf for leaf in leaves if not (leaf.startswith('中华人民共和国') and leaf[-1] in ['法', '则'])]
        return leaves

