if __name__ == '__main__':
    # config_path = sys.argv[1]
    # # DuXiaoFaCrawler.download(config_path)  # 法律条文爬取
    # with open(config_path, 'r', encoding='utf-8') as f:
    #     config = json.load(f)
    # dxf_path = config['DOWNLOAD_SAVE_PATH']
    # law_path = config['LAW_PATH']  # 格式化后的法律条文的保存路径
    # # transform.to_law(dxf_path, law_path)  # 格式化下载的法律条文
    # graph = Neo4j(law_path)
    # graph.expand('中华人民共和国刑法')
    # # TODO 直接根据法条回答简易问题
    # say = input('>>>')
    # while say != 'q':
    #     ans = graph.answer(say)  # 抢劫罪是什么？
    #     for a in ans:
    #         print(a)
    #     say = input('>>>')
    # TODO 直接根据json文件分析
    # n_law = Neo4jLaw(os.path.join('中国法律大全JSON', '刑法', '中华人民共和国刑法.json')) # 功能待实现
    pass