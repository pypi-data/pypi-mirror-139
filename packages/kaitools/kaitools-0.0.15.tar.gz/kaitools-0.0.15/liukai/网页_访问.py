# get @header @session 自动管理cookie  @禁止CA CA告警 @禁止重定向  @timeout网页访问超时 还得trycath捕捉 否则代码中间停了

import requests
import threading

# from requests.exceptions import ReadTimeout  # 这个是超时时间

from requests.packages import urllib3

# 禁用CA警告 # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   #这个好像里面的参数无效
urllib3.disable_warnings()


# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}

# s = requests.Session()  # 创建 requests.Session()对象s
# s.headers = headers  # 集成了headers   #s.headers.update(headers)  # 另外种写法

# url = 'https://www.aaa.com'
# r = s.get(url, verify=False, allow_redirects=False)  # 使用该对象s 进行get/post操作  # session已经包含了headers参数
# r = s.get(url, headers=headers, verify=False)  # 使用该对象s 进行get/post操作

# print(r.text)


class CAHRSET:
    UTF8 = "utf-8"
    GB2312 = "gb2312"


# session 是带cookies管理的
class session(object):
    s = None  # 定义一个初始化 静态变量  类属性

    single = None  # ■定义一个类属性
    single_lock = threading.Lock()  # 锁  # 创建单例session

    init_flag = False
    init_lock = threading.Lock()  # 锁   # 防止这个变量在读写的时候被多重读写了

    def __new__(cls, *args, **kwargs):
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

    def __init__(self):

        # 判断是否已经初始化过了
        with self.init_lock:
            if self.init_flag:
                print("已经初始化过了")
                return

            # 【2】 如果没初始化过
            print("这里写初始化动作的代码 ...")
            self.s = requests.Session()  # 创建 requests.Session()对象s
            self.s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}  # 集成了headers   #s.headers.update(headers)  # 另外种写法

            # 【3】结尾把已经初始化过的flag 改下标记
            self.init_flag = True

    # def get_res(self, url, verify=False, allow_redirects=False):  # 取回body
    #     # def get(self,url):
    #     self.r = self.s.get(url, verify=verify, allow_redirects=allow_redirects)
    #     return self.r

    def get(self, url, 编码=CAHRSET.UTF8, allow_redirects=True, timeout=10):  # 默认文本编码 utf-8 # 允许重定向 #取回文本
        """

        a = session()     a.get("http://www.qq.com")
        :param url:
        :param 编码:
        :param allow_redirects:
        :param timeout:  超时时间默认 10秒
        :return:

        """
        try:
            res = self.s.get(url, verify=False, allow_redirects=allow_redirects, timeout=timeout)
            return res.content.decode(编码)
        except:
            print('异常,可能是Timeout')

    def GET_取回res(self, url, allow_redirects=True, timeout=10):
        try:
            res = self.s.get(url, verify=False, allow_redirects=allow_redirects, timeout=timeout)
            return res
        except:
            print('异常,可能是Timeout')

    def GET_GB2312(self, url, allow_redirects=True, timeout=10):  # 默认utf-8
        # r = self.s.get(url, verify=False, allow_redirects=allow_redirects)
        # return r.content.decode(编码)
        return self.get(url, 编码=CAHRSET.GB2312, allow_redirects=allow_redirects, timeout=timeout)

    def GET_取二进制资源(self, url, allow_redirects=True):  # 2进制 文件 未解码为txt
        res = self.s.get(url, verify=False, allow_redirects=allow_redirects)
        return res.content

    def GET_禁止重定向(self, url):
        res = self.s.get(url, verify=False, allow_redirects=False)
        return res

    def GET_禁止重定向_取Location(self, url):
        # res = self.s.get(url, verify=False, allow_redirects=False)
        # res = self.s.get(url, verify=False, allow_redirects=False)
        # return res.headers['location']

        res = self.GET_取回res(url, allow_redirects=False)
        return self.res_取返回协议头location(res)

    def GET_禁止重定向_取Date(self, url):
        # res = self.s.get(url, verify=False, allow_redirects=False)
        # return res.headers['date']
        res = self.GET_取回res(url, allow_redirects=False)
        return self.res_取返回协议头date(res)

    @staticmethod  # python staticmethod 返回函数的静态方法。该方法不强制要求传递参数，如下声明一个静态方法：
    def res_取返回协议头date(res):
        return res.headers['date']

    @staticmethod
    def res_取返回协议头location(res):
        return res.headers['location']

    @staticmethod
    def res_取返回状态码(res):  # 200是ok的
        return res.status_code

    @staticmethod
    def res_取返回网页文本_UTF8(res, 编码=CAHRSET.UTF8):
        return res.content.decode(编码)

    @staticmethod
    def res_取返回网页文本_GB2312(res, 编码=CAHRSET.GB2312):
        return res.content.decode(编码)

    @staticmethod
    def res_取返回二进制数据(res):
        return res.content


# http  get/post  是直接访问 不带cookies管理的
class http:
    # TODO 还没开始写
    def get(self): pass

    def post(self): pass


def test_GET():
    a = session()
    print(a.get("http://www.taobao.com"))


def test_GET_GB2312页面():
    a = session()
    print(a.get("http://www.qq.com", 编码=CAHRSET.GB2312))  # 自动重定向


def test_GET_禁止重定向_取网页GMT时间():
    s = session()
    print(s)  # <__main__.session object at 0x00593150>
    print(s.GET_禁止重定向_取Date("http://www.qq.com"))
    # Tue, 01 Jun 2021 00:11:45 GMT

    a = session()
    print(a)  # <__main__.session object at 0x00593150>
    print(a.GET_禁止重定向_取Date("http://www.baidu.com"))
    # Tue, 01 Jun 2021 00:11:45 GMT
    #
    b = session()
    print(b)  # <__main__.session object at 0x00593150>
    print(b.GET_禁止重定向_取Date("http://www.baidu.com"))
    # Tue, 01 Jun 2021 00:11:45 GMT

    assert 1 == 1
