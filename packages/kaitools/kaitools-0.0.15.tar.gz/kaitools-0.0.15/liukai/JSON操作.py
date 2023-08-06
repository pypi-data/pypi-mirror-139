# 之所以不是JSON  而是JSON操作 是因为python自带json.py  import json.py会重复

import json


def json_加载(s):
    #
    try:
        s = json.loads(s)  # 反序列化 Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object.
    except:
        # print('直接进行json.loads(),捕捉到报错,重新进行json.dumps(),json.loads()进行加载')
        s = json.dumps(s)  # 序列化 Serialize obj to a JSON formatted str.
        s = json.loads(s)  # 反序列化 Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object.
    # 返回python可操作的json对象
    return s


def json_取值(json对象, key):
    return json对象[key]


def test_示例1():
    #  【1】直接取值
    # 【1】 多为网页读取回来的?不对

    s = {"currencyFundProfit": 12.58, "frozenWithDrawCash": 0.00, "currentProductAmount": 0.00,
         "toCollectPrincipal": 727739.81, "appointmentFrozenCash": 0.00, "totalAssert": 773271.85,
         "financePlanInvestAmount": 0.00, "frozenBiddingCash": 0.00, "toCollectInterest": 44278.13, "cash": 1253.91,
         "loanInvestAmount": 772017.94}

    """将 Python 对象编码成 JSON格式化string   将已编码的 JSON格式化string  解码为 Json 对象"""
    s = json.dumps(s)  # dumps   #Serialize obj to a JSON formatted str using this conversion table.
    jsonData = json.loads(s)  # Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object using this conversion table.
    print(jsonData["cash"])  # 1253.91
    assert 1 == 1


def test_示例2():
    # 【1】包含列表的取法  【2】loads  str--> Python可操作的json对象
    a = '{"status":0,"message":"ok","results":[{"name":"park","location":{"lat":39.498402,"lng":116.007069},"address":"xx road","street_id":"32541349605e7ae96ca3cc1e",' \
        '"detail":1,"uid":"32541349605e7ae96ca3cc1e"}]} '
    jsonData = json.loads(a)  # Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object using this conversion table.
    print(jsonData)
    print(jsonData['results'][0]['location']['lat'])  # 39.498402
    assert 1 == 1


def JSON_遍历(jsonData):
    for key, value in jsonData.items():  # 取得json字典的key  key是随便取的 也可以写成i
        """判断value的类型"""
        if type(value) in [int, float, str]:  # """value为int,float,str这三种类型,不能再继续解包了"""
            print('key=', key, 'value=', value)
        elif type(value) == list:  # """value为list 需要进到列表里面解包"""
            for i in value:  # 解包的i 就是子成员,一般都是dict 再对dict进行递归
                # if type(i) == dict:
                # ■★这里问题:如果列表里面就是str int这些怎么办? AttributeError: 'str' object has no attribute 'items'
                # ★更新:解包后发现是dict再递归 是str,int这些东西就算了
                if type(i) in [int, float, str]:
                    print('key=', key, 'value=', value)
                    break  # ■这种写法是 判定list里面没有继续遍历的必要,直接输出key和列表value 不再拆解
                if type(i) == dict:
                    JSON_遍历(i)  # 递归
        elif type(value) == dict:  # """value为dict字典就继续递归"""
            JSON_遍历(value)  # 递归
