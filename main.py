import os
from datetime import datetime
from utils.engine.whoosh_engine import WhooshEngine

if __name__ == '__main__':
    # NOTE:执行步骤：crawler.py->transform.py->main.py
    # with open(sys.argv[1], 'r', encoding='utf-8') as f:
    #     config = json.load(f)
    # law_path = os.path.join(config['LAW_PATH'].replace('\\', os.path.sep))  # 格式化后的法律条文的保存路径
    # graph = Neo4j(law_path, rebuild=True)
    # graph.expand('中华人民共和国刑法')
    # say = input('>>>')
    # while say != 'q':
    #     ans = graph.answer(say)  # 抢劫罪是什么？
    #     for a in ans:
    #         print(a)
    #     say = input('>>>')
    index_dir = os.path.join('data', 'LAW_INDEX')
    source_dir = os.path.join('data', '中国法律大全')
    if 0:
        WhooshEngine.create_index(index_dir, source_dir)
    start_time = datetime.now()
    answer = WhooshEngine.search_index(index_dir, "列车内抢劫会怎么样？")
    end_time = datetime.now()
    for ans in answer:
        for i in ans:
            print("%s: %s" % (i, ans[i]))
        print('-' * 10)
    if not len(answer):
        print('none')
    print("cost time: %.02f" % (end_time - start_time).total_seconds())
