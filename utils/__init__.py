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
