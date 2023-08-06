import pytest


# 定义语法
# 增
# 删
# 改
# 查


def 字典_定义():
    """
    https://www.runoob.com/python/python-dictionary.html
    dict_name = {key1 : value1, key2 : value2 }
    【1】为避免跟内置函数冲突  变量名不要使用原生函数名称 dict  包括像str list
    【2】值value可以取任何数据类型，但键key必须是不可变的，如字符串，数字或元组。
    【3】同一个key如果同时存在  后面的会覆盖前面的
    """
    # dict1 = {'a': 1, 'b': 2, 'b': '3'}  #字典包含重复键  #This inspection highlights using the same value as dictionary key twice.
    dict1 = {'a': 1, 'b': 3}  # 字典包含重复键  #This inspection highlights using the same value as dictionary key twice.
    dict2 = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    print(dict1, dict2)


# 增
def test_add():
    dic = {'a': 1, 'b': 2}
    # 字典_增(dic, k, v)
    字典_增(dic, "c", 1234567890)
    print(dic)
    assert dic == {'a': 1, 'b': 2, 'c': 1234567890}
    assert dic != {'a': 1, 'b': 2}
    with pytest.raises(AssertionError):
        assert dic == {'a': 1, 'b': 2, 'c': 3}


def 字典_增(dic, key, value):
    # 增 是直接设置key的value  立即生效
    # 一样的语法  增/改  如果key不存在就是增  key存在就是改
    dic[key] = value
    return dic  # 这里不需要返回 只是做测试


def test_字典_增_合并字典_update():
    dic1 = {'a': 1, 'b': 2}
    dic2 = {'a': 2, 'c': 3}
    dic1.update(dic2)
    print(dic1)  # {'a': 2, 'b': 2, 'c': 3}
    assert dic1 == {'a': 2, 'b': 2, 'c': 3}
    assert dic1 != {'a': 1, 'b': 2}
    # with pytest.raises(AssertionError):
    #     assert dic == {'a': 1, 'b': 2, 'c': 3}


def 字典_增_合并字典_update(dic1, dic2):
    # 把字典dict2的键 / 值对更新到dict里
    dic1.update(dic2)


def test_delete():
    dic = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    字典_删_del(dic, 'Age')
    print(dic)  # {'Name': 'Zara', 'Class': 'First'}


def 字典_删_del(dic, key):
    # dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    # del dict['Name']  # 删除键是'Name'的条目
    # dict.clear()  # 清空字典所有条目
    # del dict  # 删除字典
    del dic[key]
    return dic


def test_clear():
    dic = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    字典_删_clear(dic)
    print(dic)  # {}


def 字典_删_clear(dic):
    # 清空
    dic.clear()


def test_字典_删_pop():
    dic = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

    # 【1】 key存在 则pop成功删除 返回被删除key的value
    print(dic.pop("Name"))  # Zara
    print(dic)  # {'Age': 7, 'Class': 'First'}

    # 【2】 key不存在 pop会报错 KeyError
    with pytest.raises(KeyError):
        print(dic.pop("Name1"))

    # 【3】当Key不存在 pop的结果 会返回我们设置的None
    print(dic.pop("Name2", None))


def 字典_删_pop(dic: dict, key):
    # .pop(key[,default])
    # 删除字典给定键 key 所对应的值，返回值为被删除的值。  key值必须给出。 否则，返回default值。
    dic.pop(key)


def test_popitem():
    dic = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    dic.popitem()
    print(dic)  # {'Name': 'Zara', 'Age': 7}
    dic.popitem()
    print(dic)  # {'Name': 'Zara'}


def 字典_删_popitem(dic):
    # popitem() 返回并删除字典中的最后一对键和值。
    dic.popitem()
    return dic


def test_字典_改():
    dic = {'a': 1, 'b': 2}

    # dic['a'] = "qqq"    # 如果写在这 python检查器 会说 可以直接定义 dic = {'a': "qqq", 'b': 2} 所以搞了个小函数
    def 字典_修改():
        # dic['a'] = "qqq"
        dic['a'] = 9

    字典_修改()
    print(dic)
    assert dic == {'a': 'qqq', 'b': 2}
    assert dic != {'a': 1, 'b': 2}
    with pytest.raises(AssertionError):
        assert dic == {'a': 1, 'b': 2, 'c': 3}


def 字典_改(dic, k, newvalue):
    # 和 字典 增一样 都是直接设置值
    dic[k] = newvalue


def 字典_改_合并字典_update(dic1, dic2):
    # 同上  增
    # 把字典dict2的键 / 值对更新到dict里
    dic1.update(dic2)


def _字典_查_has_key():
    # python3_no
    #
    print("python3 没有这个语法")


def test_字典_查_取值():
    dic = {'a': 1, 'b': 2}

    print(dic['a'])  # 1
    assert dic['a'] == 1
    assert dic['a'] != 2

    # print(dic['c'])  # KeyError
    with pytest.raises(KeyError):
        assert dic['c']


def test_字典_查_取值_2():  # 字典_取值
    dic = {"a": 3, "b": "中国"}

    # 【1】断言 正确结果
    assert 字典_查_取值(dic, "a") == 3
    assert 字典_查_取值(dic, "b") == "中国"

    # 【2】断言某个异常被触发
    with pytest.raises(AssertionError):
        assert 字典_查_取值(dic, "b") == 5

    # 【3】断言?
    print("运行到这里了")
    dict2 = {1: "3"}
    print(字典_查_取值(dict2, 1))


def 字典_查_取值(dic, key):
    # 取值 # 不能加 default= 这几个字！
    return dic[key]


def test_字典_查_取值_get():
    dic = {'a': 1, 'b': 2}

    print(dic.get('a'))  # 1
    assert dic.get('a') == 1
    assert dic.get('a') != 2
    assert dic.get('c') is None

    print(dic.get('c'))  # None

    # 【3】 不能有default 这几个字
    with pytest.raises(TypeError):
        assert dic.get('c', default="nokey")  # get() takes no keyword arguments
        assert dic.get('c', default=None)  # get() takes no keyword arguments


def 字典_查_取值_get(dic, key):
    # 【1】key存在 则返回value
    # 【2】key不存在 则返回None
    # 【3】可以设置默认值 dict.get('python', 'HHHH') 返回HHHH
    # 但不能dict.get('python', default=None) 或 dict.get('python', default='HHHH'） 会直接报错
    return dic.get(key)


def 字典_查_取值_内部嵌套字典():
    dict_test = {'Name': 'Runoob', 'num': {'first_num': '66', 'second_num': '70'}, 'age': '15'}
    print(dict_test.get('first_num'))  # None
    print(dict_test.get('num').get('first_num'))  # 66


def test_字典到文本():
    dict_test = {'Name': 'Runoob', 'num': {'first_num': '66', 'second_num': '70'}, 'age': '15'}
    print(str(dict_test))  # {'Name': 'Runoob', 'num': {'first_num': '66', 'second_num': '70'}, 'age': '15'}


def test_字典到文本_2():
    # dic = {'Name': 'Runoob', 'num': {'first_num': '66', 'second_num': '70'}, 'age': '15'}
    # print(字典_到文本(dic))
    dic = {'Name': 'Runoob', 'num': '66', 'age': '15'}
    print(字典_到文本(dic))  # Name=Runoob&num=66&age=15


def 字典_到文本(dic: dict):  # 不支持嵌套这种的
    li = []
    for k, v in dic.items():
        li.append(k + "=" + v)
    return "&".join(li)


def 字典_遍历(dic):
    # 遍历  所有的key 和value
    for k, v in dic.items():
        print(k, v)

    # 1. 遍历key值
    for key in dic:
        print(key + ':' + dic[key])  # key 就是key  #value=dict[key]

    for key in dic.keys():
        print(key + ':' + dic[key])

    for value in dic.values():
        print(value)

    # 3.遍历字典项
    for kv in dic.items():
        print(kv)
    # （‘a’, '1'）(...)

    # 4.    遍历字典键值
    for key, value in dic.items():
        print(key + ':' + value)

    for (key, value) in dic.items():
        print(key + ':' + value)
