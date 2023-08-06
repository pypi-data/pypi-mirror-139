def test_数组_到文本():
    print(数组_到文本(['1', '2', 'qq'], '***'))  # 这个居然可以
    print(数组_到文本(['1', '2', 'qq'], 连接符='***'))
    print(数组_到文本(['1', '2', 'qq']))


def 数组_到文本(数组, 连接符=''):  # python 里面直接是 join
    # 原本变量名写成了list 但是内置list()方法 会导致list()失效
    return 连接符.join(数组)


def list_去重复_找重复(lis):
    重复元素_list = []
    new_list = []
    for i in lis:
        if i not in new_list:
            new_list.append(i)
        else:
            # 重复元素_list.append(i)  # 写法1 这种写法 会导致 重复的元素 会重复添加进 如果不想这么重复 可以判断是否在 重复元素_list
            if i not in 重复元素_list:
                重复元素_list.append(i)  # 写法2: 这种重复的元素 不会重复添加进来

    return new_list, 重复元素_list


def 数组_去重复_找重复(lis):
    重复元素_list = []
    new_list = []
    for i in lis:
        if i not in new_list:
            new_list.append(i)
        else:
            # 重复元素_list.append(i)  # 写法1 这种写法 会导致 重复的元素 会重复添加进 如果不想这么重复 可以判断是否在 重复元素_list
            if i not in 重复元素_list:
                重复元素_list.append(i)  # 写法2: 这种重复的元素 不会重复添加进来

    return new_list, 重复元素_list


def 数组_添加元素(li: list, n):
    return li.append(n)


def 数组_添加数组(li: list, b: list):
    return li.extend(b)


def _test_数组_删除元素_一次():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_删除元素_remove_value(li,3)
    [1, 2, 4, 3]
    >>> li == [1, 2, 4, 3]
    True
    """


def 数组_删除元素_remove_value(li: list, value):  # remove 只删1次  对li立即生效 不用返回接收 当然也可以接收
    """
    :param li:
    :param value:
    :return:
    """
    li.remove(value)
    return li


def 数组_删除元素_判断值(li: list, value):  # 会删除全部value 比如存在3个 会都删除
    new = []
    for i in li:  # 遍历li
        if i != value:  # 如果i不等于value
            new.append(i)  # 就添加进新数组
    return new


def test_数组_删除元素_pop索引():
    li=[0,1,2,3]
    print(数组_删除元素_pop索引(li, 1))  # [0, 2, 3]
    # assert dic == {'a': 1, 'b': 2, 'c': 1234567890}
    # assert dic != {'a': 1, 'b': 2}
    # with pytest.raises(AssertionError):
    #     assert dic == {'a': 1, 'b': 2, 'c': 3}

def 数组_删除元素_pop索引(li: list, n):  #
    li.pop(n)
    return  li

def 数组_删除元素_判断索引(li: list, n):  #
    new = []
    for i in range(len(li)):  # 遍历li
        if i != n:  # 如果i不等于value
            new.append(li[i])  # 就添加进新数组
    return new


def _test_数组_清空():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_清空(li)
    >>> li
    []
    """


def 数组_清空(li: list):
    li.clear()


def _test_数组_修改成员():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_修改成员(li,3,555)
    [1, 2, 555, 4, 555]
    """


def _test_填写测试函数名称():
    """
    >>> li = [1,2,3,4,3]
    [1, 2, 4, 3]
    >>> 数组_删除元素_remove_value(li,3)
    [1, 2, 4, 3]
    """


def 数组_修改成员(li: list, old_value, new_value):  # 可以接收li 也可以不接收li 是立即生效的
    """
    :param li:
    :param old_value:
    :param new_value:
    :return:
    """

    for i in range(len(li)):
        if li[i] == old_value:
            li[i] = new_value
    return li


def _test_数组_遍历_不能修改():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_遍历_不能修改(li)
    1
    2
    3
    4
    3
    """


def 数组_遍历_不能修改(li: list):
    for i in li:
        print(i)


def _test_数组_遍历_可修改():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_遍历_可修改(li)
    1
    2
    3
    4
    3
    """


def 数组_遍历_可修改(li: list):
    for i in range(len(li)):
        print(li[i])
        # 如果要修改成员的值就在这里直接改  # 一般是判断个什么 比如=某个值
        # if li[i] == old_value:
        #     li[i] = "你要改的值"


def _test_数组_修改成员_索引方式():
    """
    >>> li = [1,2,3,4,3]
    >>> 数组_修改成员_索引方式(li, 2, 5) ==[1, 2, 5, 4, 3]
    True
    >>> li
    [1, 2, 5, 4, 3]
    """


def 数组_修改成员_索引方式(li: list, 索引, new_value):  # 可接收 也可以不接收
    li[索引] = new_value
    return li


def _test_数组_合并_去重复元素():
    """
     >>> 数组_合并_去重复元素([1,2,3], [1,2,4,5,6,6])
     [1, 2, 3, 4, 5, 6]
     >>> 数组_合并_去重复元素([1,2,3], [4,5,6])
     [1, 2, 3, 4, 5, 6]
    >>> 数组_合并_去重复元素([1,2,3], [2,3,1])
    [1, 2, 3]
    >>> 数组_合并_去重复元素([], [2,3,1])
    [2, 3, 1]
    >>> 数组_合并_去重复元素([2,3,1],[])
    [2, 3, 1]
    >>> 数组_合并_去重复元素([],[])
    []
    """


def 数组_合并_去重复元素(a: list, b: list):
    for i in b:  # 遍历b
        if i not in a:  # 如果b中的元素不在a中 就添加到a中
            a.append(i)

    return a


def _test_数组_两个数组_找重复():
    """
     >>> 数组_两个数组_找重复([1,2,3], [1,2,4,5,6,6])
     [1, 2]
     >>> 数组_两个数组_找重复([1,2,3], [4,5,6])
     []
    >>> 数组_两个数组_找重复([1,2,3], [2,3,1])
    [1, 2, 3]
    >>> 数组_两个数组_找重复([], [2,3,1])
    []
    >>> 数组_两个数组_找重复([2,3,1],[])
    []
    >>> 数组_两个数组_找重复([],[])
    []
    """


def 数组_两个数组_找重复(a: list, b: list):
    result = []
    for i in a:  # 遍历a
        if i in b:  # 如果a中的元素i 同时也在b中 添加到result列表
            result.append(i)
    return result


def 数组_倒序_切片法(li):
    # 切片 [start:end:step]  step为负值时反向取值  # 步长 设置负数即可 这里设置-1
    return li[::-1]


def test_数组_移除_pop():
    li = [0,1,2,3,4]
    li.pop()
    print(li)  #[0, 1, 2, 3]
    li.pop(0)
    print(li) #[1, 2, 3]

def 数组_移除_pop(li:list):  #pop 是按索引移除 pop([index]) 如果index省略就是移除最末尾哪个  否则就是按索引移除
    li.pop()
