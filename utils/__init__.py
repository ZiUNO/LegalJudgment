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


def merge(result):
    # TODO 归并结果，获取最终合并后的结果
    result_len = len(result)
    if result_len == 1:
        return result
    middle = result_len / 2
    before_result = result[:middle]
    after_result = result[middle:]
    before_merged_result = merge(before_result)
    after_merged_result = merge(after_result)
    raw_result = before_merged_result + after_merged_result
    if isinstance(raw_result[0], dict):
        keys = list(raw_result[0].keys())
        result_value = [tuple(value for value in raw_re[key]) for key in keys for raw_re in raw_result]
        result_value = list(set(result_value))
        input(result_value)
    elif isinstance(raw_result[0], tuple):
        merged_result = None
    return merged_result
