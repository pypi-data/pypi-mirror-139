import time


def 时间_取北京时间戳(是否13位=True, 服务器index=0):
    # 功能:联网 获取北京时间

    # 参数:是否13位  --> 默认13位(毫秒级) 如果为False 则为10位时间戳(秒)
    # 参数:服务器index -->服务器序号,0是腾讯,1是阿里1688,2是百度,3是腾讯备用服务器

    # Done( 2020年11月20日)
    # 其实可以优化取北京时间戳  默认选择腾讯,第2次 服务器选择阿里 \
    #  设置参数"时间服务器序号=0" 可以指定服务器序号

    # TODO 如果实际代码有需求 可以用不同的服务器取2次 时间戳结果的差距 小于5秒即可
    # TODO 可以判断取到的值 是否准确 可以设定一个时间戳 已经过去的时间 如果<这个时间 也可以报错raise
    # TODO 如果网页访问失败 可以报错 raise

    # Done 代码:细节1:选择大厂服务器,会更稳定可靠
    # 解决方案: BATJ

    # Done 代码:细节2:减少网络资源占用
    # 原因:直接访问它们官方网址 会正常传输网页 有网络资源占用 且耗费时间
    # 解决方案:访问http地址 因为目前都升级为https 所以会自动重定向 但我们不需要 这里禁止重定向就行了

    # Done 代码:细节3: 减少代码
    # 原因:不需要解码返回的res,只取响应头中的date就行了,按格式取出来

    # Done 代码细节 响应头Date里面之所以能用文本切片,因为格式固定,且数字字母都是恒定长度:\
    # 星期固定3位字母,逗号,空格,日固定2位,月份固定3位字母等等.就是数字固定2位 年份固定4位
    # Date: Thu, 19 Nov 2020 19:55:01 GMT

    # Done 因为时间戳是相对格林威治时间经过的秒数,北京时间有8小时偏移,所以这里要加8*3600秒

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
    # url = 'http://www.qq.com'

    url_list = [
        'http://www.tencent.com',
        'http://www.1688.com',
        'http://www.baidu.com',
        'http://www.qq.com',
    ]

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    # 构造request对象  包含:url headers
    # req = urllib.request.Request(url, headers=headers)
    req = urllib.request.Request(url_list[服务器index], headers=headers)
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


def 时间_到文本(时间格式index=0, timetuple=None):
    # Done (2020年11月20日) 在版本3基础上 添加功能:时间格式 如果后续有需要 直接去list中添加对应格式
    # 时间格式index= ?
    # 0 :  N年N月N日  示例:2020年11月20日
    # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
    # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
    # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
    # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38

    # def 时间_到文本(包含时分秒=False, timetuple=None):
    # 在版本2基础上 添加功能:支持传入 时间元组  如果不传 就默认取现行时间
    # struct_time  一般由time.localtime([secs])生成 参数secs省略就是取现行时间戳time.time()
    # struct_time 被提示重名了 改成了 timetuple

    import time
    # 检查到默认时间元组为None,那么就是取现行时间      # 如果没传入时间元组 就代表取现行时间
    if timetuple is None:
        timetuple = time.localtime()
    # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)

    # 用*打散列表/元组等有序合集即可,需要几个参数它自己会传入个数,不会报错
    # N年N月N日 N时N分N秒  1=年-月-日 时:分:秒  2=年/月/日 时/分/秒  3=年月日时分秒
    # 时间格式index
    # 0 :  N年N月N日  示例:2020年11月20日
    # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
    # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
    # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
    # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
    result_list = [
        "{}年{}月{}日",
        "{}年{}月{}日{}时{}分{}秒",
        "{}年{}月{}日 {}时{}分{}秒",
        "{}-{}-{} {}:{}:{}",
        "{}/{}/{} {}/{}/{}",
    ]

    # 历史写法3
    r"""
    if 包含时分秒:
        result = "{}年{}月{}日{}时{}分{}秒"
    else:
        result = "{}年{}月{}日"
    return result.format(*timetuple)
    """

    # 历史写法3:
    r"""
    if 包含时分秒:
        result = "{}年{}月{}日{}时{}分{}秒".format(*timetuple)
    else:
        result = "{}年{}月{}日".format(*timetuple)
    return result
    """

    # 历史写法:
    r"""
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
    """

    return result_list[时间格式index].format(*timetuple)


def 时间_设置电脑时间_北京时间(服务器index=0):
    # 设置系统时间 为 北京时间  时间服务器为腾讯服务器
    # 参数:服务器index -->服务器序号,0是腾讯,1是阿里1688,2是百度,3是腾讯备用服务器
    import time
    import os

    t = time.localtime(时间_取北京时间戳(是否13位=False, 服务器index=服务器index))  # 10位时间戳 转换为 时间 元组形式
    print(t)  # time.struct_time(tm_year=2020, tm_mon=11, tm_mday=20, tm_hour=3, tm_min=0, tm_sec=28, tm_wday=4, tm_yday=325, tm_isdst=0)

    # li =list(t)[:6]  # 把元组转换成列表 list(t)  # 切片保留0~5  切片实际规则[begin=0:end=xxx)
    # cmd = r"date {}/{}/{}& time {}:{}:{}".format(*li)
    cmd = r"date {}/{}/{}& time {}:{}:{}".format(*t)

    # cmd = r"date 2015/11/25& time 11:15:00".format(t)
    # date xxx 和 time xxx 命令分别是修改日期 修改时间  # cmd命令中可以用&连接起来
    # 6个参数 用*打散放入这里  -->实际测试不用转换成列表再打散 元组直接可以打散参数的合集

    # r = os.popen(cmd)
    # print(r.read)  #: <built-in method read of _io.TextIOWrapper object at 0x0267BF30>
    os.popen(cmd)


# print(时间_取北京时间())


# demo()


t = time.time()

# print(时间_到文本(包含时分秒=True))
# print(时间_到文本(包含时分秒=False))

print(时间_取北京时间戳(服务器index=0))
print(时间_取北京时间戳(服务器index=1))
print(时间_取北京时间戳(服务器index=2))
print(时间_取北京时间戳(服务器index=3))
print(time.time() - t)

for i in range(5):
    print(时间_到文本(i))

时间_设置电脑时间_北京时间()
