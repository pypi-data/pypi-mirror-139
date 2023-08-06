# 版本: 直接调用: 时间_取北京时间戳()  时间_到文本()
def 时间_取北京时间():
    import time
    t = time.localtime(时间_取北京时间戳(是否13位=False))  # 10位时间戳 转换为 结构化时间 元组形式
    return 时间_到文本(包含时分秒=True, timetuple=t)  # 时间元组 转换:格式:xx年x月x日x时x分x秒


def 时间_取北京时间戳(是否13位=True):
    # 默认13位
    # 联网 获取北京时间
    import time
    import urllib.request

    # 禁止重定向语句  # 这里覆写了urllib.request.HTTPRedirectHandler 里面的302重定向
    class NoRedirHandler(urllib.request.HTTPRedirectHandler):
        def http_error_302(self, req, fp, code, msg, headers):
            return fp

        http_error_301 = http_error_302

    # url 列表:
    # url = 'https://www.baidu.com'
    # url = 'http://www.baidu.com/search/error.html'
    # url = 'http://www.baidu.com'
    # url = 'http://www.tencent.com'
    # url = 'http://www.1688.com'
    url = 'http://www.qq.com'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    # 构造request对象  包含:url headers
    req = urllib.request.Request(url, headers=headers)
    # opener创建
    opener = urllib.request.build_opener(NoRedirHandler)  # 这里没用cookies管理 所以只在opener这里添加了覆写的302重定向
    # opener调用request对象
    response = opener.open(req)
    # print(response.read().decode())  #不需要解码返回文本
    # h = response.info()  # 只需要取出响应头  #也不用 后面直接用  response.headers['date']就可以了
    # print("响应头", h)
    # print("Date", h["Date"])
    t = response.headers['date']
    # print('Date', t)  # Tue, 24 Sep 2019 16:44:10 GMT
    # 将日期时间字符转化为gmt_time元组
    gmt_time = time.strptime(t[5:25], "%d %b %Y %H:%M:%S")  # 截取从日期到秒 不要开头的星期和逗号空格和尾巴的GMT
    # print("gmt_time", gmt_time)
    # 将GMT时间转换成北京时间
    # time.mktime(gmt_time) 把结构化的元组 转为秒数 就是时间戳
    # time.localtime  把一个时间戳转化为struct_time元组
    # local_time = time.localtime(time.mktime(gmt_time) + 8 * 3600)
    # return
    i = time.mktime(gmt_time) + 8 * 3600
    return i * 1000 if 是否13位 else i
    # time.mktime(gmt_time) + 8 * 3600 就是北京时间戳  但是单位是秒
    # print("local_time", local_time)  # struct_time元组

    # 别人的写法:https://www.jb51.net/article/151823.htm
    # str1 = "%u-%02u-%02u" % (local_time.tm_year,local_time.tm_mon, local_time.tm_mday)
    # str2 = "%02u:%02u:%02u" % (local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
    # cmd = 'date -s "%s %s"' % (str1, str2)
    # print("cmd", cmd)  #"2019-09-25 02:10:08"

    # 我的写法:
    # print(time.strftime("%Y-%m-%d %H:%M:%S", local_time))  # 2019-09-25 02:10:08
    # print(time.strftime("%Y{}%m{}%d{}%H{}%M{}%S{}", local_time).format("年", "月", "日", "时", "分", "秒"))
    # print(时间_到文本(True, local_time))
    # return 时间_到文本(True, local_time)


# 在版本2基础上 添加功能:支持传入 时间元组  如果不传 就默认取现行时间
# struct_time  一般由time.localtime([secs])生成 参数secs省略就是取现行时间戳time.time()
# struct_time 被提示重名了 改成了 timetuple
def 时间_到文本(包含时分秒=False, timetuple=None):
    """
     #使用示例:
     >>> 时间_到文本()
     '2019年9月25日'
     >>> if None:print("其它测试")
     >>> '时' in str(时间_到文本(包含时分秒=True))  #测试是否含有关键字 '秒'
     True
     >>> '分' in str(时间_到文本(包含时分秒=True))  #测试是否含有关键字 '秒'
     True
     >>> '秒' in str(时间_到文本(包含时分秒=True))  #测试是否含有关键字 '秒'
     True
     """
    import time
    # 检查到默认时间元组为None,那么就是取现行时间      # 如果没传入时间元组 就代表取现行时间
    if timetuple is None:
        timetuple = time.localtime()

    # get 取出 指定n位 年/月/日/时/分/秒 组合 //3位就是年月日,6位就是时分秒  #自己根据需要组合长度 1~6位
    # 这里def 用到了变量struct_time 因此取到的起码不是None 要么是传进来的时间元组 要么是现行时间元组
    def _get(n, timetuple=timetuple):
        # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)
        # print(t[0]) #2019  #这种居然可行  它就是个元组方式的数据  但是注意它是int型
        # ★下面的意思是 按 2019 年 9 月 16 日 23 时 45 分 13 秒 顺序将这些文本添加进数组 再连接起来
        s = '年月日时分秒'  # list=["年","月","日"]  str也可以类似for循环进行遍历和取成员
        lis = []
        for i in range(n):
            lis.append(str(timetuple[i]))  # 整数int 转为文本型
            lis.append(s[i])
        return ''.join(lis)  # 使用列表join而不是str1+str的方式是因为好像每次+都要生成一个新的str 而将list进行join会一次性申请内存空间,更省资源

    return _get(6) if 包含时分秒 else _get(3)


def demo():
    import time
    import os

    t = time.localtime(时间_取北京时间戳(是否13位=False))  # 10位时间戳 转换为 时间 元组形式
    print(t)  # time.struct_time(tm_year=2020, tm_mon=11, tm_mday=20, tm_hour=3, tm_min=0, tm_sec=28, tm_wday=4, tm_yday=325, tm_isdst=0)

    # li =list(t)[:6]  # 把元组转换成列表 list(t)  # 切片保留0~5  切片实际规则[begin=0:end=xxx)
    # cmd = r"date {}/{}/{}& time {}:{}:{}".format(*li)
    cmd = r"date {}/{}/{}& time {}:{}:{}".format(*t)

    # cmd = r"date 2015/11/25& time 11:15:00".format(t)
    # date xxx 和 time xxx 命令分别是修改日期 修改时间  # cmd命令中可以用&连接起来
    # 6个参数 用*打散放入这里  -->实际测试不用转换成列表再打散 元组直接可以打散参数的合集

    r = os.popen(cmd)
    print(r.read)  #: <built-in method read of _io.TextIOWrapper object at 0x0267BF30>
    # os.popen(cmd)


# print(时间_取北京时间())
# TODO 其实可以优化取北京时间戳  默认选择腾讯,第2次 服务器选择阿里 \
#  设置参数"时间服务器序号=0" 可以指定服务器序号
#  这样取2次 时间戳结果的差距 小于5秒即可

demo()
