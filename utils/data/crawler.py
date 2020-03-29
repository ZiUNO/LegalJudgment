import json
import logging
import os
import pathlib
import platform
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from random import randint, shuffle

import requests
from requests import Session
from tqdm import tqdm

from utils import MultiThread, merge

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Crawler(object):
    """
    法律爬虫基类
    """

    @staticmethod
    def _threadpool_download(save_path, content):
        """
        多线程下载函数（虚静态函数）
        Args:
            save_path: 保存路径
            content: 保存内容

        Returns:

        """
        raise NotImplementedError('未重写Crawler中的_threadpool_download函数')

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
    def _threadpool_download(save_path, content):
        """
        使用线程池加速下载
        :param save_path: 文件保存目录
        :param content: 法律名
        :return:
        """
        if not pathlib.Path(save_path).exists():
            os.makedirs(save_path)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
        try:
            response = requests.get('http://www.baidu.com/s?ie=UTF-8&wd=%s' % content, headers=header)
            results = response.text
            r = re.compile(
                u'<a href="(http[s]?://www.baidu.com/link.*?)" target="_blank"><em>%s</em>.*?_百度知识图谱' % content)
            url = r.findall(results)[0]
        except:
            print('CANNOT FIND %s ON DuXiaoFa' % content)
            return
        url = url.replace("http", "https")
        response = requests.head(url, headers=header)
        results = response.headers['location']
        cid = re.sub('.*?cid=', '', results)
        url = 'https://duxiaofa.baidu.com/law/Ajax/detail?type=statute&cid=%s' % cid
        txt = requests.get(url, headers=header).text.encode().decode('unicode_escape')

        json_law = json.loads(txt, strict=False)
        save_file_name = os.path.join(save_path, '%s.json' % content)
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
                executor.submit(DuXiaoFaCrawler._threadpool_download, os.path.join(save_path, law_label), law)
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


invalid_uniqid = []


class SoLegalCaseCrawler(Crawler):

    @staticmethod
    def _threadpool_download(save_path, content):
        uniqid = content
        file_path = os.path.join(save_path, uniqid + '.json')
        # print("TO DOWNLOAD %s ... " % uniqid, end='')
        if pathlib.Path(file_path).exists():
            # print("EXIST")
            return
        url = "https://solegal.cn/api/v2/authcase/detail?uniqid=%s" % uniqid
        proxy_list = [
            {"https": "https://125.123.123.150:9000"},
            {"https": "https://125.123.126.133:9000"},
            {"https": "https://124.232.133.199:3128"},
            {"https": "https://119.39.68.130:808"},
            {"https": "https://182.61.175.77:8118"},
            {"https": "https://59.38.60.105:9797"},
            {"https": "https://115.233.210.218:808"},
            {"https": "https://58.250.23.210:1080"},
            {"https": "https://59.38.61.173:9797"},
            {"https": "https://113.247.252.114:9090"},
            {"https": "https://59.38.63.148:9797"},
            {"https": "https://60.205.159.195:3128"},
            {"https": "https://121.238.1.175:8118"},
            {"https": "https://14.20.235.117:808"},
            {"https": "https://59.38.62.168:9797"},
            {"https": "https://183.129.207.80:21776"},
            {"https": "https://116.62.215.123:8118"},
            {"https": "https://183.129.207.93:13629"},
            {"https": "https://218.77.120.31:8888"},
            {"https": "https://59.37.18.243:3128"},
            {"https": "https://124.205.143.213:32612"},
            {"https": "https://223.243.252.155:65309"},
            {"https": "https://124.205.155.152:9090"},
            {"https": "https://124.152.32.140:53281"},
            {"https": "https://122.228.19.9:3389"},
            {"https": "https://14.20.235.82:9797"},
            {"https": "https://114.99.10.55:808"},  # invalid
            {"https": "https://222.189.190.166:9999"},
            {"https": "https://123.169.34.238:808"},  # invalid
            {"https": "https://218.249.45.162:35586"},  # invalid
            {"https": "https://114.239.145.166:808"},
            {"https": "https://163.204.246.205:9999"},  # invalid
            {"https": "https://210.5.10.87:53281"},
            {"https": "https://117.68.194.91:18118"},
            {"https": "https://114.239.144.53:808"},
            {"https": "https://114.99.11.213:23760"},
            {"https": "https://175.148.71.214:1133"},  # invalid
            {"https": "https://117.69.201.61:40196"},
            {"https": "https://163.125.70.180:9999"},
            {"https": "https://182.35.85.60:9999"},
            {"https": "https://60.167.21.135:27393"}
        ]
        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        shuffle(proxy_list)
        for proxies in tqdm(proxy_list, desc="TESTING FOR %s" % uniqid):
            try:
                with Session() as s:
                    case_content = s.get(url=url, proxies=proxies, headers=headers).json()["data"]["contents"]
            except Exception:
                continue
            if len(case_content) == 0:
                return
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(case_content, f, ensure_ascii=False)
            print("DONE")
            return
        invalid_uniqid.append(uniqid)

    @staticmethod
    def download(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        if platform.system() == "Windows":
            save_path = r'..\\..\\' + config['CASE_PATH']
        else:
            save_path = os.path.join('..', '..', config['CASE_PATH'].replace("\\", os.path.sep))
        if not pathlib.Path(save_path).exists():
            os.mkdir(save_path)
        kinds = ['刑事', '民事', '行政']
        save_path_kind_uniqid = os.path.join(save_path, 'uniqid.json')
        kind_cases_uniqid = {kind: [] for kind in kinds}
        if pathlib.Path(save_path_kind_uniqid).exists():
            with open(save_path_kind_uniqid, 'r', encoding='utf-8') as f:
                kind_cases_uniqid = json.load(f)
        url_authcase = u"https://solegal.cn/api/v2/authcase/search?q=%s&offset=%d&count=%d"
        user_cookie = input("USER COOKIE(NEED USER COOKIE TO DOWNLOAD CASES)[null]:", )
        if user_cookie == "":
            user_cookie = '1=1'
        user_cookie = [one_cookie.strip().split("=") for one_cookie in user_cookie.split(';')]
        user_cookie = {one_cookie[0]: one_cookie[1] for one_cookie in user_cookie}
        once_count = 20
        total_count = 2000
        for keyword in kinds:
            if len(kind_cases_uniqid[keyword]) != 0:
                continue
            for now_count in tqdm(range(0, total_count, once_count), desc="DOWNLOAD KIND UNIQID OF %s" % keyword):
                tmp_url_authcase = url_authcase % (keyword, now_count, once_count)
                try:
                    authcase_json = requests.get(tmp_url_authcase, cookies=user_cookie, timeout=3.0).json()
                except Exception:
                    continue
                time.sleep(randint(3, 5))
                authcase_results = authcase_json["data"]["results"]
                if not len(authcase_results):
                    continue
                _ = [kind_cases_uniqid[keyword].append(authcase["uniqid"]) for authcase in authcase_results]
            for _ in tqdm(range(randint(10, 30)), desc='SLEEP TIME'):
                time.sleep(1)
        if pathlib.Path(save_path_kind_uniqid).exists():
            os.remove(save_path_kind_uniqid)
        with open(save_path_kind_uniqid, 'w', encoding='utf-8') as f:
            json.dump(kind_cases_uniqid, f, ensure_ascii=False)
        executor = ThreadPoolExecutor()
        for keyword in tqdm(kinds, desc='DOWNLOAD CASES'):
            dir_path = os.path.join(save_path, keyword)
            if not pathlib.Path(dir_path).exists():
                os.mkdir(dir_path)
            for uniqid in tqdm(kind_cases_uniqid[keyword], desc="DOWNLOAD UNIQID OF %s" % keyword):
                # SoLegalCaseCrawler._threadpool_download(dir_path, uniqid)
                executor.submit(SoLegalCaseCrawler._threadpool_download, dir_path, uniqid)
        executor.shutdown(True)


class Proxy(object):
    url = r"https://www.xicidaili.com/wn/"  # 西刺代理HTTPS
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    def __init__(self, speed=0.80, connection_time=0.80, update=False):
        proxy_data = requests.get(url=Proxy.url, headers=Proxy.headers).text
        if proxy_data != "":
            self.__pages = int(re.findall('<a href="/wn/[0-9]*?">([0-9]*?)</a> <a class', proxy_data, re.S)[0])
        else:
            self.__pages = 0  # pages == 0: ip is blocked
        self.__speed = int(speed * 100)
        self.__connection_time = int(connection_time * 100)

    def __iter__(self):
        proxy_ips = []
        if not self.__pages:
            with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..', 'data', 'proxy.json'), 'r',
                      encoding='utf-8') as f:
                proxy_ips = json.load(f)["ips"]
        else:
            for i in tqdm(range(self.__pages), desc="[crawler]-[__iter__]-GET PROXY IPS"):
                try:
                    proxy_data = requests.get(url=Proxy.url + str(i + 1), headers=Proxy.headers).text
                except Exception:
                    continue
                if proxy_data == "":
                    logger.info('local ip is blocked, auto save ips to file and return ips that have been saved')
                    break
                time.sleep(randint(2, 5))
                proxy_data = re.findall(u"<tr class.*?>(.*?)</tr>", proxy_data, re.S)
                proxy_data = [re.findall(
                    u'<td class="country">.*?<td>([\.0-9]*?)</td>\s*<td>([0-9]*?)</td>.*?width:([0-9]*)%.*?width:([0-9]*)%">',
                    proxy, re.S)[0] for proxy in proxy_data]
                proxy_data = [{"https": "https://%s:%s" % (proxy[0], proxy[1])} for proxy in proxy_data
                              if int(proxy[2]) >= self.__speed and int(proxy[3]) >= self.__connection_time]
                proxy_ips += proxy_data
            with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..', 'data', 'proxy.json'), 'w',
                      encoding='utf-8') as f:
                json.dump({"ips": proxy_ips}, f, ensure_ascii=False, indent=4)
        return iter(proxy_ips)


def get_synonyms(words):
    url = u"https://www.cilin.org/jyc/w_%s.html"
    synonyms = {}
    if isinstance(words, str):
        words = [words]
    logger.info('***** Get synonyms *****')
    for word in tqdm(words, desc="Get synonyms"):
        get_data = None
        for _ in range(100):
            try:
                get_data = requests.get(url % word, timeout=3.0)
            except Exception:
                to_sleep = randint(1, 5)
                # print("[exception] sleep: %d(s)" % to_sleep)
                time.sleep(to_sleep)
                continue
            break
        if get_data is None or get_data.status_code != 200:
            about_words = [word]
        else:
            html = get_data.content.decode('utf-8')
            about_words = re.findall(u'<b>近义词</b><br>汉语:(.*?)<br>', html, re.S)
            if len(about_words) == 0:
                about_words = [word]
            else:
                about_words = "\n".join(about_words)
                about_words = re.sub(u"<.*?>", "", about_words)
                about_words = re.findall(u"([\u4e00-\u9fa5]*)", about_words, re.S)
                about_words = [tmp_word.strip() for tmp_word in about_words if tmp_word.strip() != ''] + [word]
        # print(word, about_words)
        synonyms[word] = list(set(about_words))
        # print(" download %s: %s" % (word, synonyms[word]))
    return synonyms


def get_similar_cases(keywords):
    def get_similar_case(keyword):
        url_case = u"https://solegal.cn/api/v2/case/search?q=%s" % keyword
        url_authcase = u"https://solegal.cn/api/v2/authcase/search?q=%s" % keyword
        try:
            case_json = requests.get(url_case).json()
            authcase_json = requests.get(url_authcase).json()
        except Exception:
            return {"authcase": [], "case": []}
        case_results = case_json["data"]["results"]
        authcase_results = authcase_json["data"]["results"]
        keep_words = {"uniqid": "uniqid", "TITLE": "title", "baseList": "baseList"}
        authcase = [{keep_words[key]: result[key] for key in keep_words} for result in authcase_results]
        case = [{keep_words[key]: result[key] for key in keep_words} for result in case_results]
        similar_case = {"authcase": authcase, "case": case}
        return similar_case

    threads = []
    similar_cases = []
    logger.info('***** Get similar cases *****')
    for keyword in tqdm(keywords, desc="Create keywords threads"):
        keyword_thread = MultiThread(get_similar_case, args=(keyword,))
        keyword_thread.start()
        threads.append(keyword_thread)
    _ = [thread.join() for thread in tqdm(threads, desc="End Keywords threads")]
    _ = [similar_cases.append(thread.get_result()) for thread in threads]
    similar_cases = merge(similar_cases)
    # similar_cases = {
    #     "authcase": [
    #         {
    #             "uniqid": "f02b1fc6-e8ad-4730-a26a-f7a94ef34f8b",
    #             "title": "重庆市渝中区人民检察院诉朱波伟、雷秀平抢劫案",
    #             "baseList": ["《最高人民法院公报》  2006年第4期(总:114期)", "重庆市渝中区人民法院"]
    #         },
    #         {
    #             "uniqid": "1c0337d0-51d3-45ff-a389-cfbca11a3fca",
    #             "title": "检例第23号：蔡金星、陈国辉等（抢劫）不核准追诉案",
    #             "baseList": ["最高人民检察院"]
    #         }
    #     ],
    #     "case": [
    #         {
    #             "uniqid": "7baf7d60-a40f-4d4a-800d-c5a7758d507e",
    #             "title": "常斌抢劫罪、寻衅滋事罪刑罚与执行变更刑事裁定书",
    #             "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更558号", "2018-02-01"]
    #         },
    #         {
    #             "uniqid": "50c7c56b-4419-4b79-8cac-83f9dd33db9e",
    #             "title": "武俊肥故意杀人罪、抢劫罪等刑罚与执行变更刑事裁定书",
    #             "baseList": ["河北省沧州市中级人民法院", "（2018）冀09刑更607号", "2018-02-01"]
    #         }
    #
    #     ]
    # }
    return similar_cases


if __name__ == '__main__':
    config_path = os.path.join('..', '..', 'config.json')
    # DuXiaoFaCrawler.download(config_path)  # 法律条文爬取
    # print(get_synonyms(["盗窃", "抢劫罪"]))
    start_time = time.time()
    # similar_cases = get_similar_cases(["盗窃", "抢劫罪"])
    # print(similar_cases)
    SoLegalCaseCrawler.download(config_path)
    print("cost time: %.02f" % (time.time() - start_time))
    with open(os.path.join('..', '..', 'data', '案例', 'invalid_uniqid.json'), 'w', encoding='utf-8') as f:
        json.dump(invalid_uniqid, f, ensure_ascii=False, indent=2)

    # proxy = Proxy(update=True)
    # count = 0
    # for p in proxy:
    #     count += 1
    #     if count == 100:
    #         break
    #     print(p)
