from utils.data.neo4j import Neo4j

if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    law_path = r'..\\..\\data\\中国法律大全JSON'  # 格式化后的法律条文的保存路径
    graph = Neo4j(law_path, rebuild=True)
    graph.expand('中华人民共和国刑法')
    say = input('>>>')
    while say != 'q':
        ans = graph.answer(say)  # 抢劫罪是什么？
        for a in ans:
            print(a)
        say = input('>>>')
