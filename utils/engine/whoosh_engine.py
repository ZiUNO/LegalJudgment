import os
import pathlib

from jieba.analyse import ChineseAnalyzer
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.sorting import FieldFacet


def create_in_for_dir(index_dir, source_dir):
    with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], '中文停用词表.txt'), 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    stopwords = set([stopword.strip() for stopword in stopwords])
    analyser = ChineseAnalyzer(stopwords)
    schema = Schema(title=TEXT(stored=True, analyzer=analyser), path=ID(stored=True), content=TEXT(analyzer=analyser))
    ix = create_in(index_dir, schema, indexname="law_index")
    writer = ix.writer()
    # TODO 使用writer.add_document将每个法律大全中的文件加入到索引中
    # 例：writer.add_document(title='title', path="path", content="content")
    writer.commit()


if __name__ == '__main__':
    index_dir = os.path.join('..', '..', 'data', 'LAW_INDEX')
    source_dir = os.path.join('..', '..', 'data', '中国法律大全')

    create_in_for_dir(index_dir, source_dir)

    index = open_dir(index_dir, indexname="law_index")
    new_list = []
    with index.searcher() as searcher:
        parser = QueryParser("条文检索", index.schema)
        query = parser.parse("搜索的关键字")
        facet = FieldFacet("content", reverse=True)  # 按序排列搜索结果
        results = searcher.search(query, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10
        for result1 in results:
            print(dict(result1))
            new_list.append(dict(result1))
