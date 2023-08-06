# logging模块 单例模式
# ■线程安全:多线程下也不会产生多个logger对象
# ■未知:多线程的读写是否安全

# ■调用方法:
#  log = log_single()  # 获取logger对象入口log_single()  传递给log变量 后续log.xx调用即可  见下面.
#  log.warning("警告")  # 默认级别是info debug等级小于info 不会被记录
#  log.error("错误")
#  log.info("提示")
#  log.debug("查错")

import logging
import logging.handlers
import os
import threading


# https://www.cnblogs.com/huchong/p/8244279.html
# 好像多线程 确实会出问题  类的创建还没发现 但是init出现了   正在执行相关初始化动作  出现了不止1次
# 因为从执行初始化动作到init_flag =True 是有间隔的

class _log_single(object):  # ■提供1个线程安全的单例logger  给log_single()函数使用
    # class _log_single():  # ■提供1个线程安全的单例logger  给log_single()函数使用
    single = None  # ■定义一个类属性
    init_flag = False

    single_lock = threading.Lock()  # 锁
    init_lock = threading.Lock()  # 锁

    def __new__(cls, *args, **kwargs):
        # ■ 重写 __new__ 方法
        # ■ cls表示这个类本身。 my? 是的  --> 下面的print(cls,"cls")  # <class '__main__.my'> cls

        # ■锁 包含 整个分配内存空间的过程
        with cls.single_lock:
            if cls.single is None:  # 如果该类属性是None 就要分配空间
                # cls.single = super().__new__(cls, *args, **kwargs)
                cls.single = super().__new__(cls)
                # cls.single = super(_log_single).__new__(cls)
                # cls.single = super().__new__(cls) 等同于 cls.single = object.__new__(cls) --> 因为class my(): 等同于 class my(object): 省略了父类 object
                # ■ 因为重写__new__方法  导致没有自动分配内存空间的语句 这里要分配 所以要调用父类的__new__方法
                # ■ super().__new__(cls) 调用 父类super() 的 __new__()方法 分配内存空间 给cls(也就是my这个类本身)分配空间
                # ■ 默认参数就是 cls  cls 是my这个类本身

            # print(cls,"cls")  # <class '__main__.my'>
            # print(cls.single)  # <__main__.my object at 0x00592230>
            return cls.single

    def __init__(self):  # self表示一个具体的实例本身。如果用了staticmethod，那么就可以无视这个self，将这个方法当成一个普通的函数使用。

        # 判断是否已经初始化过了
        with self.init_lock:

            # 【1】
            if self.init_flag:
                print("已经初始化过了")
                return

            # 【2】 ■□这里写 执行 初始化 动作代码  ....
            print("这里写初始化动作的代码 ...")
            # TOD...

            # print(__file__)  # C:/Users/Administrator/PycharmProjects/s9/s9/测试_logging模块/single_log.py
            # os.path.basename(filePath) 从全路径获取文件名
            # __name__  是 main

            filename = __file__  # 完整路径  C:/Users/Administrator/PycharmProjects/s9/s9/测试_logging模块/single_log.py
            filename = os.path.basename(filename)  # 文件名 single_log.py
            filename, extension = os.path.splitext(filename)  # python  分离文件名和后缀
            filename = filename + ".log"

            logger = logging.getLogger(__name__)
            # logger.setLevel(logging.DEBUG)
            logger.setLevel(logging.INFO)

            # f = logging.handlers.TimedRotatingFileHandler(filename="./MyLog/" + filename, when='MIDNIGHT', interval=1,backupCount=0, encoding="utf-8")
            f = logging.handlers.TimedRotatingFileHandler(filename=filename, when='MIDNIGHT', interval=1, backupCount=0, encoding="utf-8")

            # f.setLevel(logging.DEBUG)  # 每个句柄单独设置级别  fh.setLevel(logging.DEBUG)
            f.setLevel(logging.INFO)  # 每个句柄单独设置级别  fh.setLevel(logging.DEBUG)
            f.suffix = "%Y-%m-%d.log"  # 设置滚动日志的后缀

            formatter = logging.Formatter('%(asctime)s - [%(filename)s] - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
            f.setFormatter(formatter)  # 绑定日志格式到句柄f
            logger.addHandler(f)  # 句柄 添加到logger对象

            print(logger, "class 里面 logger")

            self.logger = logger  # 把logger 传给类自身的属性  外面调用可以_log().log

            # ■初始化后修改init_flag值 # ■放在这里的话 多线程调试能明显发现 出现了很多次 执行初始化动作的 操作
            # 【3】
            self.init_flag = True


def log_single():
    return _log_single().logger


if __name__ == '__main__':
    # def get_log():
    #     return mylog().logger

    log = log_single()
    log1 = log_single()  # -->报错 为什么   TypeError: 'Logger' object is not callable  -->因为之前写法是log=log() 这样log就变成函数入口了 log()就是调用log()()了
    # log1= _log().log
    log.debug("log")
    # log = mylog()
    # print(log,"mylog")
    # log = mylog().logger
    # print(log,"mylog().logger")
    # log1 = mylog().logger
    # print(log1,"mylog().logger")
    log.warning("警告")
    log.info("提示")
    log.error("错误")
    log.debug("查错")
    print(log, "log")
    print(log1, "log1")
    log1.debug("log1")

    #
    # i = 0
    # # while i < 100000000:
    # # i = i + 1
    # for i in range(100000000):
    #     time.sleep(0.1)
    #     log.error("记录" + str(i))
