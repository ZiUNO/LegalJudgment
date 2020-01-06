import jieba
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HandleQ(object):
    url = u"https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet"
    end = "charset=%s&access_token=%s"
    charset = "UTF-8"
    has_init = False
    config = {
        "API Key": None,
        "Secret Key": None
    }
    access_token = None
    headers = {
        'Content-Type': 'application/json'
    }
    host = r'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'

    def __new__(cls, config):
        if not cls.has_init:
            jieba.initialize()
            for key in config:
                cls.config[key] = config[key]
            response = requests.get(cls.host % (cls.config["API Key"], cls.config["Secret Key"]), timeout=3)
            json_response = response.json()
            try:
                cls.access_token = json_response["access_token"]
            except KeyError:
                raise RuntimeError("[handleq]-[__new__]-BAIDU AUTHENTICATION FAILED")
            cls.end = cls.end % (cls.charset, cls.access_token)
        return object.__new__(cls)

    def __init__(self, q):
        if not HandleQ.has_init:
            HandleQ.has_init = True
            return
        assert len(q) <= 200, "[handleq]-[__init__]-LENGTH OF q IS %d (>200)" % len(q)
        self.__q = q
        # PILE handle_q
        # TODO - 1 q -> 纠正错别字 -> correct_q
        correct_q_json = requests.post(url="%s?%s" % (HandleQ.url, HandleQ.end),
                                       headers=HandleQ.headers, json={"text": q}, timeout=3).json()
        self.__correct_q = correct_q_json["item"]["correct_query"]
        self.__vec_fragment = correct_q_json["item"]["vec_fragment"]
        """
        vec_fragment (baidu)
        ori_frag: string 原片段
        correct_frag: double 替换片段
        begin_pos: int 起始(长度单位)
        end_pos: list 结尾(长度单位)
        """
        self.__lcut_correct_q = jieba.lcut(self.__correct_q, cut_all=False)  # FIXME 可能调整cut_all=True
        # self.__final_q = None
        # self.__keywords = None
        # self.__keywords_of_lcut_correct_q = None
        # self.__map_q = None
        # self.__highlight = None
        # self.__final_q_highlight = None

    @property
    def lcut_final_q(self):
        return jieba.lcut(self.__final_q, cut_all=False)  # FIXME 可能调整cut_all=True

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
