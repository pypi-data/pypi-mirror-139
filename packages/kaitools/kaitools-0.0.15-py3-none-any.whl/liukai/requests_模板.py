# ■□注意 这里面没弄timeout 但实际要弄的

def get_模板():  # get @header @session 自动管理cookie  @禁止CA CA告警 @禁止重定向
    import requests

    from requests.packages import urllib3
    # 禁用CA警告 # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   #这个好像里面的参数无效
    urllib3.disable_warnings()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}
    s = requests.Session()  # 创建 requests.Session()对象s
    s.headers = headers  # 集成了headers   #s.headers.update(headers)  # 另外种写法

    # 带session了 后面只需要这下面的重复
    url = 'https://www.aaa.com'
    r = s.get(url, verify=False, allow_redirects=False)  # 使用该对象s 进行get/post操作  # session已经包含了headers参数
    # r = s.get(url, headers=headers, verify=False)  # 使用该对象s 进行get/post操作

    print(r.text)


def post_模板():  # post @header @session 自动管理cookie

    import requests
    from requests.packages import urllib3
    # 禁用CA警告 # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)   #这个好像里面的参数无效
    urllib3.disable_warnings()

    s = requests.Session()  # 创建 requests.Session()对象
    s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"}
    # 集成headers

    # 带session了 后面只需要这下面的重复
    url = 'https://www.aaa.com'
    postdata = {'key1': 'value1', 'key2': 'value2'}  # 这里是字典
    # postdata="key1=value1&key2=value2"  也支持文本
    r = s.post(url, data=postdata)  # 使用该对象 进行get/post操作

    print(r.text)
