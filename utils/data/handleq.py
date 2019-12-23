class HandleQ(object):

    def __init__(self, q):
        self.__q = q
        # TODO - 1 q -> 纠正错别字 -> correct_q
        self.__correct_q = q
        # TODO - 2 correct_q -> 分词 -> lcut_correct_q
        self.__lcut_correct_q = [tmp for tmp in self.__correct_q]

        self.__final_q = q
        self.__keywords = None
        self.__keywords_of_lcut_correct_q = None
        self.__map_q = []
        self.__highlight = []
        self.__final_q_highlight = []

    @property
    def correct_q(self):
        return self.__correct_q

    @property
    def lcut_correct_q(self):
        return self.__lcut_correct_q

    @property
    def final_q(self):
        return self.__final_q

    @property
    def keywords_of_lcut_correct_q(self):
        return self.__keywords_of_lcut_correct_q

    @keywords_of_lcut_correct_q.setter
    def keywords_of_lcut_correct_q(self, value):
        assert len(value) == len(self.__lcut_correct_q)
        self.__keywords = [word for word in value if word is not None]
        self.__keywords_of_lcut_correct_q = value
        # TODO - 3 keywords_of_lcut_correct_q + lcut_correct_q -> 合并 -> final_q
        self.__final_q = None
        # TODO - 4 q + final_q -> 字一一映射 -> map_q ==> 单线程
        self.__map_q = []
        # TODO - 5 keywords_of_lcut_correct_q + q -> 遍历位置 -> highlight
        self.__highlight = []

    @property
    def keywords(self):
        return self.__keywords  # ["抢劫", "盗窃"]

    @property
    def highlight(self):
        return self.__highlight

    @property
    def final_q_highlight(self):
        return self.__final_q_highlight

    @final_q_highlight.setter
    def final_q_highlight(self, value):
        self.__final_q_highlight = value
        # TODO - 6 final_q_highlight + q + map_q -> 反向映射 -> 更新 highlight
        self.__highlight = [0, 2, 3]
