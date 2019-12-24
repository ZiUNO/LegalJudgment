import json
import os
import pathlib
import platform
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from random import randint

import requests
from tqdm import tqdm


class Crawler(object):
    """
    法律爬虫基类
    """

    @staticmethod
    def download(config_path):
        """
        下载函数（虚静态函数）
        :param config_path:配置文件路径（包括保存路径及法律分类名称）
        """
        raise NotImplementedError('未重写Crawler中的download函数')


class DuXiaoFaCrawler(Crawler):
    """
    度小法（百度）爬虫
    """

    @staticmethod
    def __threadpool_download(save_path, law):
        """
        使用线程池加速下载
        :param save_path: 文件保存目录
        :param law: 法律名
        :return:
        """
        if not pathlib.Path(save_path).exists():
            os.makedirs(save_path)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
        try:
            response = requests.get('http://www.baidu.com/s?ie=UTF-8&wd=%s' % law, headers=header)
            results = response.text
            r = re.compile(
                u'<a href="(http[s]?://www.baidu.com/link.*?)" target="_blank"><em>%s</em>.*?_百度知识图谱' % law)
            url = r.findall(results)[0]
        except:
            print('CANNOT FIND %s ON DuXiaoFa' % law)
            return
        url = url.replace("http", "https")
        response = requests.head(url, headers=header)
        results = response.headers['location']
        cid = re.sub('.*?cid=', '', results)
        url = 'https://duxiaofa.baidu.com/law/Ajax/detail?type=statute&cid=%s' % cid
        txt = requests.get(url, headers=header).text.encode().decode('unicode_escape')

        json_law = json.loads(txt, strict=False)
        save_file_name = os.path.join(save_path, '%s.json' % law)
        with open(save_file_name, 'w', encoding='utf-8') as f:
            json.dump(json_law, f, ensure_ascii=False)
        print('SAVING TO %s...' % save_file_name)

    @staticmethod
    def download(config_path):
        """
        爬取度小法中的法律条文（重写父类中的下载函数）
        :param config_path: 下载配置文件所在的路径
        """
        starttime = time.time()
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        if platform.system() == "Windows":
            save_path = r'..\\..\\' + config['DOWNLOAD_SAVE_PATH_DXF']
        else:
            save_path = os.path.join('..', '..', config['DOWNLOAD_SAVE_PATH_DXF'].replace("\\", os.path.sep))
        laws = config['LAW_NAME']
        total_law = []
        executor = ThreadPoolExecutor(max_workers=4)
        for law_label in laws:
            for law in laws[law_label]:
                executor.submit(DuXiaoFaCrawler.__threadpool_download, os.path.join(save_path, law_label), law)
                total_law.append(law)
        executor.shutdown(True)
        total = len(total_law)
        count = 0
        for law_label in laws:
            for law in laws[law_label]:
                if pathlib.Path(os.path.join(save_path, law_label, law + '.json')).exists():
                    count += 1
                    total_law.remove(law)
        print('cost time: %d' % (time.time() - starttime))
        timestamp = int(time.time())
        print('timestamp %d->%d' % (config['TIMESTAMP'], timestamp))
        config['TIMESTAMP'] = timestamp
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)
        print("total: %d, success: %d, failed: %d, success rate=%.02f" % (total, count, total - count, count / total))
        print('CANNOT FIND:')
        _ = [print(law) for law in total_law]


def get_synonyms(words):
    url = u"https://www.cilin.org/jyc/w_%s.html"
    synonyms = {}
    if isinstance(words, str):
        words = [words]
    for word in tqdm(words, desc="GET SYNONYMS"):
        get_data = None
        for _ in range(100):
            try:
                get_data = requests.get(url % word, timeout=3.0)
            except Exception:
                to_sleep = randint(1, 5)
                print("[exception] sleep: %d(s)" % to_sleep)
                time.sleep(to_sleep)
                continue
            break
        if get_data is None or get_data.status_code != 200:
            continue
        html = get_data.content.decode('utf-8')
        about_words = re.findall(u'<b>近义词</b><br>汉语:(.*?)<br>', html, re.S)
        if len(about_words) == 0:
            continue
        about_words = "\n".join(about_words)
        about_words = re.sub(u"<.*?>", "", about_words)
        about_words = re.findall(u"([\u4e00-\u9fa5]*)", about_words, re.S)
        about_words = tuple(set([tmp_word.strip() for tmp_word in about_words if tmp_word.strip() != '']))
        # print(word, about_words)
        synonyms[word] = about_words
    return synonyms


if __name__ == '__main__':
    # config_path = os.path.join('..', '..', 'config.json')
    # DuXiaoFaCrawler.download(config_path)  # 法律条文爬取
    print(get_synonyms(["盗窃", "抢劫罪"]))
