import logging

import jieba
import jieba.posseg as pseg
import requests

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
    pseg_ignore = None

    def __new__(cls, config):
        if not cls.has_init:
            logger.info('***** HandleQ Initializing *****')
            jieba.initialize()
            baidu_config = config["baidu"]
            for key in baidu_config:
                cls.config[key] = baidu_config[key]
            response = requests.get(cls.host % (cls.config["API Key"], cls.config["Secret Key"]), timeout=3)
            json_response = response.json()
            try:
                cls.access_token = json_response["access_token"]
            except KeyError:
                logger.error('Baidu authentication failed')
                raise RuntimeError()
            cls.end = cls.end % (cls.charset, cls.access_token)
            cls.pseg_ignore = config["pseg_ignore"]
            logger.info('***** HandleQ End of initialization *****')
        return object.__new__(cls)

    def __init__(self, q):
        self.__lcut_final_q = []
        if not HandleQ.has_init:
            HandleQ.has_init = True
            return
        assert len(q) <= 200
        logger.info('***** HandleQ *****')
        logger.info(' Question: %s' % q)
        self.__q = q
        correct_q_json = requests.post(url="%s?%s" % (HandleQ.url, HandleQ.end),
                                       headers=HandleQ.headers, json={"text": q}, timeout=3).json()
        self.__correct_q = correct_q_json["item"]["correct_query"]
        logger.info(' Correct question: %s' % self.__correct_q)
        self.__vec_fragment = correct_q_json["item"]["vec_fragment"]
        """
        vec_fragment (baidu)
        ori_frag: string 原片段
        correct_frag: double 替换片段
        begin_pos: int 起始(长度单位)
        end_pos: list 结尾(长度单位)
        """
        self.__lcut_correct_q = []
        word_with_flag = pseg.cut(self.__correct_q, use_paddle=True)
        for word, flag in word_with_flag:
            if flag in HandleQ.pseg_ignore:
                continue
            self.__lcut_correct_q.append(word)
        logger.info(' Lcut correct question: %s' % str(self.__lcut_correct_q))
        self.__final_q = None
        self.__keywords = None
        self.__keywords_of_lcut_correct_q = None
        self.__map_q = None
        self.__highlight = None
        self.__final_q_highlight = None

    @property
    def correct_q(self):
        logger.info(' Correct question: %s' % str(self.__correct_q))
        return self.__correct_q

    @property
    def lcut_correct_q(self):
        logger.info(' Lcut correct question: %s' % str(self.__lcut_correct_q))
        return self.__lcut_correct_q

    @property
    def final_q(self):
        logger.info(' Final question: %s' % str(self.__final_q))
        return self.__final_q

    @property
    def keywords_of_lcut_correct_q(self):
        logger.info(' Keywords of lcut correct question: %s' % str(self.__keywords_of_lcut_correct_q))
        return self.__keywords_of_lcut_correct_q

    @keywords_of_lcut_correct_q.setter
    def keywords_of_lcut_correct_q(self, value):
        assert len(value) == len(self.__lcut_correct_q)
        self.__keywords = list(set([word for word in value if word is not None]))
        self.__keywords_of_lcut_correct_q = value
        # self.__final_q = "".join([word
        #                           if self.__keywords_of_lcut_correct_q[i] is None
        #                           else self.__keywords_of_lcut_correct_q[i]
        #                           for i, word in enumerate(self.__lcut_correct_q)])
        self.__final_q = self.__correct_q
        word_with_flag = pseg.cut(self.__final_q, use_paddle=True)
        for word, flag in word_with_flag:
            if flag in HandleQ.pseg_ignore:
                continue
            self.__lcut_final_q.append(word)
        # self.__map_q = [(self.__lcut_correct_q[i], self.__keywords_of_lcut_correct_q[i]) for i in
        #                 range(len(self.__keywords_of_lcut_correct_q))]  # map_q [('偷窃', '窃得'),...]
        self.__highlight = [self.__lcut_correct_q[i] for i in range(len(self.__lcut_correct_q)) if
                            self.__keywords_of_lcut_correct_q[i] is not None]

    @property
    def keywords(self):
        logger.info(' Keywords: %s' % str(self.__keywords))
        return self.__keywords

    @property
    def highlight(self):
        logger.info(' Highlight: %s' % str(self.__highlight))
        return self.__highlight

    @property
    def final_q_highlight(self):
        logger.info(' Final question highlight: %s' % str(self.__final_q_highlight))
        return self.__final_q_highlight

    @final_q_highlight.setter
    def final_q_highlight(self, value):
        self.__final_q_highlight = self.__highlight = value
