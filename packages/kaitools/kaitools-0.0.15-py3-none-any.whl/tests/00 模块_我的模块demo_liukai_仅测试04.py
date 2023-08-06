# 测试41212121
# 12121212


# 正则  #文本_取中间文本   文本_取中间文本
def 文本_取中间文本(string, front, behind):
    import re
    # search 只查1次  #符合条件就停止
    # re.search(正则表达式,str,re.S)会返回一个对象,然后对该对象使用.group(i)方法
    # .group() 等同 .group(0) 返回匹配的全部对象到一起?
    # .group(1) ~ .group(n) 分别存储每个匹配到的内容? 不是  当使用括号就表示认为分组了 比如(.*?) 因为group(0) 用来存储 已经被占用  所以分组按顺序存放于.group(1) ~ .group(n)
    # r=re.search(front + '(.*?)' + behind, str, re.S)
    # print(r)
    # print(r.span())
    # for i in r: print(i)  #错误:TypeError: '_sre.SRE_Match' object is not iterable

    print(re.search(front + '(.*?)' + behind, string, re.S))  # <_sre.SRE_Match object; span=(0, 4), match='1234'>
    # res =re.search(front + '(.*?)' + behind, str, re.S).group() #1234
    print(re.search(front + '(.*?)' + behind, string, re.S).groups())  # 1234  ('4',)
    print(re.search(front + '(.*?)' + behind, string, re.S).group())  # 1234
    # for i in  res:print (i)
    print(re.search(front + '(.*?)' + behind, string, re.S).group(0))  # 1234
    print(re.search(front + '(.*?)' + behind, string, re.S).group(1))  # 23
    # print(re.search(front + '(.*?)' + behind, str, re.S).group(2))   #23
    # # print(re.search(front + '(.*?)' + behind, str, re.S).group(2))   #23  IndexError: no such group
    #
    # return re.search(front + '(.*?)' + behind, str, re.S).group(1)    #23


print(bool(None))  # False
print(bool(''))  # False
# print('string'+None)   # 【1】报错

# print(文本_取中间文本("1234",'1','4'))
# print(文本_取中间文本("1234",'1','5'))
# print(文本_取中间文本("123456789",'23','5'))
print(文本_取中间文本("12345678923012345", '23', '5'))


