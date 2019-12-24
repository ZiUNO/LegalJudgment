import jieba


class HandleQ(object):

    def __init__(self, q):
        # PILE handle_q
        self.__q = q
        # TODO - 1 q -> 纠正错别字 -> correct_q
        self.__correct_q = q
        self.__lcut_correct_q = jieba.lcut(self.__correct_q, cut_all=False)  # FIXME 可能调整cut_all=True
        self.__final_q = None
        self.__keywords = None
        self.__keywords_of_lcut_correct_q = None
        self.__map_q = None
        self.__highlight = None
        self.__final_q_highlight = None

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
        self.__keywords = list(set([word for word in value if word is not None]))
        self.__keywords_of_lcut_correct_q = value
        self.__final_q = "".join([word
                                  if self.__keywords_of_lcut_correct_q[i] is None
                                  else self.__keywords_of_lcut_correct_q[i]
                                  for i, word in enumerate(self.__lcut_correct_q)])
        self.__map_q = [(self.__lcut_correct_q[i], self.__keywords_of_lcut_correct_q[i]) for i in
                        range(len(self.__keywords_of_lcut_correct_q))]  # map_q [('偷窃', '窃得'),...]
        # TODO - 5 keywords_of_lcut_correct_q + q -> 遍历位置 -> highlight
        self.__highlight = [self.__lcut_correct_q[i] for i in range(len(self.__lcut_correct_q)) if
                            self.__keywords_of_lcut_correct_q[i] is not None]

    @property
    def keywords(self):
        return self.__keywords

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
        self.__highlight = value
