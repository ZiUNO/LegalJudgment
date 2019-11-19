import os
import pathlib

import jieba
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.sorting import FieldFacet


class WhooshEngine(object):
    __stopwords = None

    @classmethod
    def load_stopwords(cls, stopwords_path='中文停用词表.txt'):
        with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], stopwords_path), 'r',
                  encoding='utf-8') as f:
            stopwords = f.readlines()
        stopwords = set([stopword.strip() for stopword in stopwords])
        cls.__stopwords = stopwords

    @classmethod
    def create_index(cls, index_dir, source_dir):
        if cls.__stopwords is None:
            cls.load_stopwords()
        analyser = ChineseAnalyzer(cls.__stopwords)

        schema = Schema(title=TEXT(stored=True, analyzer=analyser), path=ID(stored=True),
                        content=TEXT(analyzer=analyser))
        if not pathlib.Path(index_dir).exists():
            os.makedirs(index_dir)
        ix = create_in(index_dir, schema)
        writer = ix.writer()

        def create(writer, source):
            if len(set(os.listdir(source)).difference({'title.txt', 'content.txt'})) == 0:
                content = ''
                title_path = os.path.join(source, 'title.txt')
                content_path = os.path.join(source, 'content.txt')
                if pathlib.Path(title_path).exists():
                    with open(title_path, 'r', encoding='utf-8') as f:
                        content += f.read()
                if pathlib.Path(content_path).exists():
                    with open(content_path, 'r', encoding='utf-8') as f:
                        content += f.read()
                print("CREATING INDEX FOR ITEM %s ..." % source)
                writer.add_document(title=source.split(os.path.sep)[-1], path=source, content=content)
                return
            for file_dir in os.listdir(source):
                path = os.path.join(source, file_dir)
                if pathlib.Path(path).is_dir():
                    create(writer, path)
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print("CREATING INDEX FOR %s ..." % path)
                    writer.add_document(title=file_dir[:-4], path=path, content=content)

        create(writer, source_dir)
        writer.commit()

    @classmethod
    def search_index(cls, index_dir, ques):
        if cls.__stopwords is None:
            cls.load_stopwords()

        def read(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content.strip()

        index = open_dir(index_dir)
        new_list = []
        answer = []
        stopwords = cls.__stopwords
        with index.searcher() as searcher:
            parser = QueryParser("content", index.schema)
            ques = " ".join(list(set(jieba.lcut_for_search(ques)).difference(stopwords)))
            # TODO 会怎么样在分词过程中会被分为“会”“怎么样”-》需要分词或称中自行更新停用词
            query = parser.parse(ques)
            facet = FieldFacet("content", reverse=True)  # 按序排列搜索结果
            results = searcher.search(query, limit=None, sortedby=facet)
            for result in results:
                new_list.append(dict(result))
        for result in new_list:
            path = result["path"]
            title = result["title"]
            answer_from = path.split(os.path.sep)
            answer_from = [ans for ans in answer_from if ans not in {'..', 'data', 'title', 'content', '[PIECE]'}]
            *answer_from, answer_no = answer_from
            # each answer : {'from': '', 'no': ''[, 'title': ''][, 'content': '']}
            new_answer = {'from': answer_from, 'no': answer_no}
            if title == answer_no:
                title_path = os.path.join(path, 'title.txt')
                content_path = os.path.join(path, 'content.txt')
                if pathlib.Path(title_path).exists():
                    new_answer['title'] = read(title_path)
                if pathlib.Path(content_path).exists():
                    new_answer['content'] = read(content_path)
            else:
                new_answer[title] = read(path)
            answer.append(new_answer)
        return answer
