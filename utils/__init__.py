from threading import Thread


class MultiThread(Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.__func = func
        self.__args = args
        self.__result = None

    def run(self):
        self.__result = self.__func(*self.__args)

    def get_result(self):
        return self.__result


class Result(object):
    def __init__(self, result):
        self.__result = {key: {str(list(single_result.values())): single_result
                               for single_result in result[key]}
                         for key in result}

    def __add__(self, other):
        # TODO 结果相加直接返回结果
        final_result = {}
        keys = list(self.__result.keys())
        assert keys == list(other.__result.keys())
        for key in keys:
            self_key_result_set = set(self.__result[key].keys())
            other_key_result_set = set(other.__result[key].keys())
            intersection = self_key_result_set.intersection(other_key_result_set)
            final_result[key] = [self.__result[key][inter] for inter in intersection] \
                if len(intersection) \
                else list(self.__result[key].values()) + list(other.__result[key].values())
        return final_result


def merge(result):
    # TODO 归并结果，获取最终合并后的结果
    result_len = len(result)
    if result_len == 1:
        return result[0]
    middle = result_len // 2
    before_result = result[:middle]
    after_result = result[middle:]
    before_merged_result = merge(before_result)
    after_merged_result = merge(after_result)
    before_result = Result(before_merged_result)
    after_result = Result(after_merged_result)
    result = before_result + after_result
    return result


def display(results):
    for i, result in enumerate(results):
        print("%d " % i + "-" * 50)
        for key in result:
            print("%s " % key + "*" * 20)
            for keep in result[key]:
                for tmp_key in keep:
                    print("%s: " % tmp_key, keep[tmp_key])


if __name__ == '__main__':
    results = [
        {
            'authcase': [
                {'uniqid': '51cef0c0-5579-4173-8f66-aa8369d5aa07',
                 'title': '许某峰未成年盗窃前科封存后成年时再盗窃不应作为盗窃惯犯处理案', 'baseList': ['江苏省东台市人民法院']},
            ],
            'case': [
                {'uniqid': '156e76f2-760a-48f6-b9b3-e03aa1f0fe98',
                 'title': '许文华盗窃一审刑事判决书',
                 'baseList': ['广东省开平市人民法院', '（2016）粤0783刑初366号', '2016-10-28']},
                {'uniqid': '2f6552a0-687b-4a86-ac99-622b61e1982e',  # # # 3
                 'title': '邱建良盗窃一审刑事判决书',
                 'baseList': ['浙江省湖州市南浔区人民法院', '（2017）浙0503刑初295号', '2017-07-20']},
                {'uniqid': 'afd125e5-0317-4ee7-9958-f34ac647274b',  # # # # 4
                 'title': '德某、佰某盗窃一审刑事判决书',
                 'baseList': ['湖北省武汉市江岸区人民法院', '（2016）鄂0102刑初1223号', '2016-11-20']}]
        },
        {
            'authcase': [
                {'uniqid': '5f7f3744-5705-4775-91ec-7e2c150223d9',
                 'title': '广东省肇庆市人民检察院诉梁克财等抢劫案',
                 'baseList': ['《最高人民法院公报》 2010年第6期(总第164期)', '广东省高级人民法院']},
                {'uniqid': '4e07b1df-0134-457a-b422-37fbf6c6b748',  # # 2
                 'title': '马明义、韩国良、马明利盗窃抗诉案',
                 'baseList': ['《最高人民检察院公报》 1996年第4号(总第34号)', '青海省高级人民法院']},
                {'uniqid': '99aa4679-15bd-4a8a-a19d-41e1e9a4e29c',
                 'title': '汤彪虎、汤红旗、凌平华、邓飞、张杰、宋南平抢劫、流氓案',
                 'baseList': ['《最高人民检察院公报》 1998年第1号(总第42号)', '湖南省株洲市中级人民法院']}],
            'case': [
                {'uniqid': '2f6552a0-687b-4a86-ac99-622b61e1982e',  # # # 3
                 'title': '邱建良盗窃一审刑事判决书',
                 'baseList': ['浙江省湖州市南浔区人民法院', '（2017）浙0503刑初295号', '2017-07-20']},
                {'uniqid': '6d36aab7-54e2-4da7-b025-578a44a0ce25',
                 'title': '石一石格减刑刑事裁定书',
                 'baseList': ['四川省凉山彝族自治州中级人民法院', '（2018）川34刑更2110号', '2018-09-06']},
                {'uniqid': 'afd125e5-0317-4ee7-9958-f34ac647274b',  # # # # 4
                 'title': '德某、佰某盗窃一审刑事判决书',
                 'baseList': ['湖北省武汉市江岸区人民法院', '（2016）鄂0102刑初1223号', '2016-11-20']}
            ]
        }
    ]
    print(merge(results))
