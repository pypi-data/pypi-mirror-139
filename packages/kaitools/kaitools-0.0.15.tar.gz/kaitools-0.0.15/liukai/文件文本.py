import os
import shutil


def 文本_取部分文本_前面(string, endstring):
    """
    >>> string = "0123456789"
    >>> 文本_取部分文本_前面(string, "56")
    '01234'
    """
    # 比如 0123456789  里面 要取出56前面的部分:01234
    # 返回值:None 或者 符合条件的string

    pos = string.find(endstring)  # 取:后面文本的起始位置

    if pos == -1:  # 如果没找到 返回 None
        return None

    return string[:pos]  # 返回 切片


def 文本_取部分文本_后面(string, startstring):
    """
    >>> string = "0123456789"
    >>> 文本_取部分文本_后面(string, "56")
    '789'
    """

    # 比如 0123456789  里面 要取出56后面的部分:789
    # 返回值:None 或者 符合条件的string

    pos = string.find(startstring)  # 取:标识文本的起始位置

    if pos == -1:
        return None

    pos = pos + len(startstring)  # 截取的位置 应该以标识文本出现的位置+它自己的长度
    # 比如0123456789 56出现的位置是5 截取的位置应该是 5+文本长度2 正好是7

    return string[pos:]


def 文件_到list(file, 分隔符="\n"):
    import os

    li = []  # 判断文件的路径是否存在

    # 如果文件不存在 直接返回 空的列表
    if not os.path.isfile(file):
        return li

    # 下面就是文件存在的处理
    txt = 文件_读入文本(file)
    li = txt.split(分隔符)  # li = txt.split("\n")
    return li


def list_写到文件(li: list, file, 分隔符="\n"):
    # 这里没处理file是相对路径时 文件夹是否存在的问题吗? --> 在文本_写到文件里面
    text = 分隔符.join(li)
    文本_写到文件(file, text)


def 文件_取出字典(filepath):  # 文件_取出字典
    # def load_dict_from_file(filepath):  # 文件_取出字典
    dict_ = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                dict_[key] = value
    # except IOError as ioerr:
    except IOError:
        print("文件 %s 不存在" % filepath)

    return dict_


def 字典_写到文件(_dict, filepath):  # 字典_写到文件
    # def 字典_到文件(_dict, filepath):  # 字典_写到文件
    try:
        with open(filepath, 'w') as f:
            for key, value in _dict.items():
                f.write('%s:%s\n' % (key, value))
    # except IOError as IOError:
    except IOError:
        print("文件 %s 无法创建" % filepath)


def 文件_是否存在__(file, 只判断文件=True):
    # import pathlib
    # return pathlib.Path(file).is_file()
    # 方法1:
    # import pathlib
    # print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
    # print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行
    # 方法2:
    # import os
    # print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
    # print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
    import os
    if 只判断文件:
        return os.path.isfile(file)  # 只判断文件
    else:
        return os.path.exists(file)  # 该路径只要存在,无论是文件还是文件夹,都可以


# 文本_读入文本   #一.文件不存在   二.文件编码是gbk /文件编码是utf8
def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()


def 文件_写入文本(file, text):  # 朝文件中写东西
    文本_写到文件(file, text)


def 文件_是否存在(path):
    import os
    return os.path.isfile(path)  # 这里需要是绝对路径 相对路径无法判断 -->3.6版本好像可以接受相对路径


def 文件_删除(filepath):  # 只能删除单个文件  os.remove(filepath)
    import os
    # filepath = 'f:/123.txt'
    if os.path.exists(filepath):
        os.remove(filepath)


def 文件_取运行目录():
    return os.getcwd()  # 当前xx.py文件的目录


def test_文件夹_遍历():
    文件夹_遍历文件(r"C:\新建文件夹")


def 文件夹_遍历文件(directory):
    # 【1】在遍历过程中会全部处理到  深入N层
    # 【2】 这种方式只组合文件  输出的路径 是文件的完整路径 不是文件夹的

    for root, dirs, files in os.walk(directory):  # fileroot ,dirnames,filenames
        for file in files:  # 这里只对文件操作 也可以改为对dirs进行操作
            print(os.path.join(root, file))  # 【1】 完整路径  root 与 file连接
            # print(file)  # 【2】 仅文件名 无路径
            # 【3】 这里可以写一些操作 比如加入新的待操作数组 重命名移动什么的  也可以当时就移动
            r""" 文件夹遍历 + 批量移动的操作
            
            if ".txt" in file:
                old = os.path.join(root, file)  # 老的 文件路径
                # new = "D:\PycharmProjects\sign_appium\爬虫_kanxiaoshuo_支持批量_分开存放\html" + "\\" + file
                # new_txt_dir = r"D:\小说_H"
                new = new_txt_dir + "\\" + file  # 新的 文件路径
                shutil.move(old, new)  # 移动文件
                
            """


def 文件夹_遍历文件夹(directory):
    # 【1】在遍历过程中会全部处理到  深入N层
    # 【2】 这种方式只组合文件  输出的路径 是文件的完整路径 不是文件夹的

    # directory =r"C:\新建文件夹"
    for root, dirs, files in os.walk(directory):  # fileroot ,dirnames,filenames
        for d in dirs:  # 这里只对文件操作 也可以改为对dirs进行操作
            print(os.path.join(root, d))  # 【1】 完整路径  root 与 file连接
    # C:\新建文件夹\文件夹1
    # C:\新建文件夹\文件夹2
    # C:\新建文件夹\文件夹4
    # C:\新建文件夹\文件夹1\子文件夹1
    # C:\新建文件夹\文件夹2\文件夹2_子


def 文件夹_遍历_只当前层(rootdir):
    # 列出文件夹下所有的目录与文件 # 仅名字
    # 如果要组成完整路径可以用 fori遍历 期间 os.path.join(rootdir, i)

    # rootdir = r"C:\新建文件夹"
    li = os.listdir(rootdir)
    print(li)
    # ['哼哼哈嘿.测试', '文件1 - 副本.txt', '文件1.txt', '文件2.txt', '文件夹1', '文件夹2', '文件夹4', '文本123_被移动文件.txt', '测试_']


def 文件夹_遍历_方法2(rootdir):
    # 方法: 因为os.listdir(rootdir):只遍历当前目录 我们可以在判断当前是文件夹的时候 进行递归调用
    for i in os.listdir(rootdir):
        path = os.path.join(rootdir, i)
        print(path)
        if os.path.isdir(path):
            文件夹_遍历_方法2(path)


def 文件夹_遍历_可打印目录树文本(rootDir, level=1):
    if level == 1:
        print(rootDir)
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print('│  ' * (level - 1) + '│--' + lists)
        if os.path.isdir(path):
            文件夹_遍历_可打印目录树文本(path, level + 1)
    r"""
    rootdir = r"C:\新建文件夹"
    文件夹_遍历_可打印目录树文本(rootDir)
    
    C:\新建文件夹
    │--哼哼哈嘿.测试
    │--文件1 - 副本.txt
    │--文件1.txt
    │--文件2.txt
    │--文件夹1
    │  │--子文件夹1
    │  │  │--3
    │  │--子文件文件1.txt
    │  │--子文件文件3333.txt
    │  │--子文件文件3333_.txt
    │--文件夹2
    │  │--文件夹2_子
    │  │  │--文件夹2_子_子.txt
    │  │--文件夹2_子.rtf
    │  │--文本123_新移动文件.txt
    │--文件夹4
    │--文本123_被移动文件.txt
    │--测试_
    """


r''' python删除文件或文件夹
import os
os.remove(path)  # path是文件的路径，如果这个路径是一个文件夹，则会抛出OSError的错误，这时需用用rmdir()来删除
os.rmdir(path)  # path是文件夹路径，注意文件夹需要时空的才能被删除
os.unlink('F:\新建文本文档.txt')  # unlink的功能和remove一样是删除一个文件，但是删除一个删除一个正在使用的文件会报错。
'''


def 文件夹_删除(path):  # 这个好 不用自己写  虽然自己写实现了
    # shutil 方法
    shutil.rmtree(path)  # 递归删除一个目录以及目录内的所有内容
    # 还有参数 ignore_errors


def 文件夹_删除_自己写的(path):
    # os.rmdir(path)
    import os
    文件夹_清空(path)  # 先遍历清空 子文本 和 子目录
    # os.removedirs(path)
    os.rmdir(path)  # 删除自己这个文件夹


def 文件夹_清空(path):
    # 【1】最后只剩下自己这个文件夹

    import os
    # top - - 根目录下的每一个文件夹(包含它自己), 产生3 - 元组(dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。
    # topdown - topdown 为真，则优先遍历top目录，否则优先遍历top的子目录(默认为开启)
    # -可选，为True或者没有指定, 一个目录的的3 - 元组将比它的任何子文件夹的3 - 元组先产生(目录自上而下)。
    #   如果topdown为    False, 一个目录的3 - 元组将比它的任何子文件夹的3 - 元组后产生(目录自下而上)。

    # TODO 它的流程是探到底 有文件夹 就一直探
    # 探到目录下没目录了 就开始   因为代码是先删文件  删完回来把自己这个目录删掉
    # 再去探 平级的下一个目录 也是一样

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:  # 先删文件
            print(os.path.join(root, name))
            os.remove(os.path.join(root, name))
        for name in dirs:  # 再删文件夹  # ■□这里有点迷糊 如果它下面有文件呢?
            print(os.path.join(root, name))
            os.rmdir(os.path.join(root, name))

    r''' 清空流程
    c:\新建文件夹 - 副本\文件夹1\子文件夹1\3
    c:\新建文件夹 - 副本\文件夹1\子文件文件1.txt
    c:\新建文件夹 - 副本\文件夹1\子文件文件3333.txt
    c:\新建文件夹 - 副本\文件夹1\子文件文件3333_.txt
    c:\新建文件夹 - 副本\文件夹1\子文件夹1
    c:\新建文件夹 - 副本\文件夹2\文件夹2_子\文件夹2_子_子.txt
    c:\新建文件夹 - 副本\文件夹2\文件夹2_子.rtf
    c:\新建文件夹 - 副本\文件夹2\文本123_新移动文件.txt
    c:\新建文件夹 - 副本\文件夹2\文件夹2_子
    c:\新建文件夹 - 副本\哼哼哈嘿.测试
    c:\新建文件夹 - 副本\文件1 - 副本.txt
    c:\新建文件夹 - 副本\文件1.txt
    c:\新建文件夹 - 副本\文件2.txt
    c:\新建文件夹 - 副本\文本123_被移动文件.txt
    c:\新建文件夹 - 副本\测试_
    c:\新建文件夹 - 副本\文件夹1
    c:\新建文件夹 - 副本\文件夹2
    c:\新建文件夹 - 副本\文件夹4
    '''


def 文件夹_是否存在(path):
    import os
    return os.path.isdir(path)


def 文件夹_创建(path):
    import os
    if not os.path.isdir(path):  # 文件夹不存在
        os.makedirs(path)  # 文件夹 创建
    # ■□调试版:
    # if os.path.isdir(path):
    #     print(path,"已经存在")
    # else:
    #     print(path,"不存在,即将创建")
    #     os.makedirs(path)


def 文件_是否存在___废弃(file, 只判断文件=True):
    # ■废弃原因:因为  os.path.isfile 直接可以判断 同时 文件夹 是否存在做了另外个函数

    # import pathlib
    # return pathlib.Path(file).is_file()
    # 方法1:
    # import pathlib
    # print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
    # print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行
    # 方法2:
    # import os
    # print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
    # print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
    import os
    if 只判断文件:
        return os.path.isfile(file)  # 只判断文件
    else:
        return os.path.exists(file)  # 该路径只要存在,无论是文件还是文件夹,都可以


def 文件路径_取_名称_后缀(path):
    # ■后缀格式如".py" ".txt" 包含"."符号
    import os
    # ■这里无法分离相对路径的 需要转换为绝对路径
    path = os.path.realpath(path)  # 转换为绝对路径
    path_dir, path_fname = os.path.split(path)  # 取文件夹名和文件名
    filename, extension = os.path.splitext(path_fname)  # 取文件名前面和后缀
    return filename, extension


def 文件路径_取_目录_文件名(path):
    import os
    # ■这里无法分离相对路径的 需要转换为绝对路径
    path = os.path.realpath(path)  # 转换为绝对路径
    path_dir, path_fname = os.path.split(path)
    return path_dir, path_fname


def 文件路径_取目录(path):
    import os
    return os.path.dirname(os.path.realpath(path))


def 文件路径_取文件名(path):
    import os
    return os.path.basename(os.path.realpath(path))


def 文件_更名(file_oldname, file_newname):
    # os.renames(old, new)
    import os
    # 【1】 需要判断文件是否存在 old文件 要存在  //如果不存在 就返回
    if not os.path.isfile(file_oldname):
        print(file_oldname, "not exist!")
        return

    # os.rename(old_file_path, new_file_path), 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
    # os.renames(old_file_path, new_file_path), 是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名
    os.renames(file_oldname, file_newname)


def 文件_改名(file_oldname, file_newname):
    文件_更名(file_oldname, file_newname)


def 文件_重命名(file_oldname, file_newname):
    文件_更名(file_oldname, file_newname)


def 文件_移动(old, new, override=True):
    """

    :param old:
    :param new:
    :param override:  默认覆盖
    :return:
    """
    import os
    import shutil
    # shutil.move(old, new)  # 移动文件  基本写法

    # 1. old文件 要存在  //如果不存在 就返回
    if not os.path.isfile(old):
        print(old, "not exist!")
        return

    # 2. 如果new文件已经 存在 如何处理? 覆盖? shutil.move 是会覆盖的
    if os.path.isfile(new):
        if override:
            print(new, " exist!", "将要覆盖")
        else:
            print(new, " exist!", "不继续覆盖")
            return  # 这里如果不覆盖 就return

    # 3. new文件 所在文件夹要存在  //如果不存在 要创建
    new_dir, new_filename = os.path.split(new)  # 分离目标路径的 文件夹和文件名
    if not os.path.isdir(new_dir):  # 如果 目标文件夹 不存在
        print(new_dir, "not exist!")
        os.makedirs(new_dir)  # 创建 文件夹

    shutil.move(old, new)  # 移动 文件
    print("文件_移动  {} -> {}".format(old, new))


def _test_文本_取字符串左边():
    """
    >>> 文本_取字符串左边("0123456","34")
    '012'
    >>> 文本_取字符串左边("0123456","012")
    ''
    >>> 文本_取字符串左边("0123456","333")  # 当子文本 不存在于 string中
    ''
    """


def 文本_取字符串左边(文本: str, 字符串):
    """
    文本_取字符串左边("0123456","34")       '012'
    :param 文本:
    :param 字符串:
    :return:
    """
    pos = 文本.find(字符串)  # 这个pos必须判断 否则会造成>>> 文本_取字符串左边("0123456","333") 切片为[:-1] '012345'
    if pos > -1:
        return 文本[:pos]
    return ""


def _test_文本_取字符串右边():
    """
    >>> 文本_取字符串右边("0123456","34")
    '56'
    >>> 文本_取字符串右边("0123456","012")
    '3456'
    >>> 文本_取字符串右边("0123456","56")
    ''
    >>> 文本_取字符串右边("0123456","333")  # 当子文本 不存在于 string中
    ''
    """


def 文本_取字符串右边(文本: str, 字符串):
    """
    文本_取字符串右边("0123456","34")       '56'
    """
    pos = 文本.find(字符串)  # 这个pos必须判断 否则会造成>>> 文本_取字符串左边("0123456","333") 切片为[:-1] '012345'
    if pos > -1:
        return 文本[pos + len(字符串):]
    return ""


def 文本_取左边部分(文本: str, 字符串):
    return 文本_取字符串左边(文本, 字符串)


def 文本_取右边部分(文本: str, 字符串):
    return 文本_取字符串右边(文本, 字符串)


def _test_文本_取子文本位置_倒找():
    """
    >>> 文本_取子文本位置_倒找('abcdefga', "a")
    7
    >>> 文本_取子文本位置_倒找('012345670123', "012")
    8
    """


def 文本_取子文本位置_倒找(文本: str, 子文本):
    return 文本.rfind(子文本)


def 文本_去首尾空(string: str):
    return string.strip()


def 文本_是否以指定字符开头(文本: str, 子文本):
    return 文本.startswith(子文本)


def 文本_是否以指定字符结尾(文本: str, 子文本):
    return 文本.endswith(子文本)


def 文本_取长度(文本):
    return len(文本)
    # str='ABCDEF'
    # print(len(str))  #6


def 文本_截取(文本: str, start, end):  # 就是切片  其他语言中的sub
    # end为截止标识  不包括end所在位置
    return 文本[start:end]


def 文本_切片(文本: str, start, end):
    # end为截止标识  不包括end所在位置    # 同截取
    return 文本[start:end]


def 文本_子文本是否存在(文本: str, 子文本):
    return 子文本 in 文本
    # if  "a" in "abc"


def test_文本_子文本是否存在_find方式():
    print(-1 is False)  # False
    print(-1 is True)  # False


def 文本_子文本是否存在_find方式(文本: str, 子文本):
    # 方式2  也可以用 find来判断
    return 文本.find(子文本) > -1


def 文本_写到文件(file, text):
    # 覆盖式写入
    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)


# 文本_追加文本  #往文件 追加 不是覆写  可选参数:结尾是否添加换行符 默认为真
def 文本_追加文本(file, data, mode=True):
    """
    file:文件路径
    data:追加的数据
    mode:结尾是否增加换行,默认为假 -->改为默认为真
    """

    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    # 追加方式  "a+" 打开文件
    with open(file, mode="a+", encoding='utf-8') as f:
        # 如果模式==True 添加自动换行  模式==False 直接追加文本
        f.write(data + '\n') if mode else f.write(data)


def 文本_取中间_批量(string, front, behind):
    # 返回值 : [] 或 [string1,string2,...]
    # 示例:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
    # 示例:文本_取中间_批量('0123450123445','236','5') -->>[]

    lis = []

    start_pos = 0
    while True:
        front_pos = string.find(front, start_pos)

        if front_pos == -1:
            break

        start_pos = front_pos + len(front)  # 修改 find文本 起始位置

        behind_pos = string.find(behind, start_pos)

        if behind_pos == -1:
            break

        lis.append(string[start_pos:behind_pos])  # 加入列表

        start_pos = behind_pos + len(behind)  # 修改 find文本 起始位置 为 后面文本的下一个

    return lis


def 文本_取中间文本(string, front, behind):
    # 返回值:None 或者 符合条件的string

    front_pos = string.find(front)

    if front_pos == -1:
        return None

    start_pos = front_pos + len(front)  # 修改 find文本 起始位置

    behind_pos = string.find(behind, start_pos)

    if behind_pos == -1:
        return None

    return string[start_pos:behind_pos]


def 文本_取子文本_正则search(string, 正则表达式):
    import re
    # r = re.search(正则表达式, string, re.S)  # 这个是只找1次的那种
    return re.findall(正则表达式, string, re.S)  # 返回列表


def _test_文本_取子文本_正则findall():
    """
    >>> string = "abcdefgbcdefg"
    >>> 文本_取子文本_正则findall(string,"bc.*?fg")
    ['bcdefg', 'bcdefg']
    >>> 文本_取子文本_正则findall(string,"bc.*fg")
    ['bcdefgbcdefg']
    >>> 文本_取子文本_正则findall(string,"bc(.*?)fg")
    ['de', 'de']
    """


def 文本_取子文本_正则findall(string, 正则表达式):
    import re
    # r = re.search(正则表达式, string, re.S)  # 这个是只找1次的那种
    return re.findall(正则表达式, string, re.S)  # 返回列表


# 正则  #文本_取中间文本   文本_取中间文本
def 文本_取中间文本_正则_(string, front, behind):
    # ■□2020年10月20日更新: 涉及元字符转义 不推荐
    # def 文本_取中间文本(string, front, behind, 标识自动转义=False):
    # 返回值:None 或者 str1
    # 示例1:文本_取中间文本('0123450123445','23','5') -->> '4'
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>None
    import re
    # search 只查1次  #符合条件就停止
    # re.search(正则表达式,string,re.S)会返回一个对象,然后对该对象使用.group(i)方法  #备注:这里是因为正则有分组(.*?) 所以才是.group(1)
    # print(re.search(front + '(.*?)' + behind, string, re.S))
    # print(re.search(front + '(.*?)' + behind, string, re.S).group(0))
    # return re.search(front + '(.*?)' + behind, string, re.S).group(1)   #■★bug:当无匹配时,返回值None是没有group方法的

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    '''
    if 标识自动转义:
        for i in ".*?()[]":
            if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
            if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
            # front = re.sub('[%s]' % i, "\\" + i, front)
            # behind = re.sub('[%s]' % i, "\\" + i, behind)
            # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
    '''
    for i in ".*?()[]+-":  # TODO 可能还有问题 因为元字符 还包括 xxxxxxxxxxx 等等
        # front = front.replace(i, "\\" + i)
        # behind = behind.replace(i, "\\" + i)
        if i in front:
            front = front.replace(i, "\\" + i)
        if i in behind:
            behind = behind.replace(i, "\\" + i)
        # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错
    #  ■ 之所以要转义  是因为比如 (121977522)要取(和)之间的文本 使用front + '(.*?)' + behind就出错了

    r = re.search(front + '(.*?)' + behind, string, re.S)
    return r.group(1) if r else None  # 问题:这里是否要改成""? 因为很多时候 是str1+str2+..这种组合来的?
    # return r.group(1) if r else r   #因为当r为None时 return r 等同于None


# 文本_取中间_批量   #正则
def 文本_取中间_批量_正则_(string, front, behind):
    # ■□2020年10月20日更新: 涉及元字符转义 不推荐
    # def 文本_取中间_批量(string, front, behind, 标识自动转义=False):
    # 返回值:[] 或者 [str1,str2,...]
    # 示例1:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>[]
    """
    >>> 文本_取中间_批量('0123450123445','23','5')
    ['4', '44']
    >>> 文本_取中间_批量('0123450123445','236','5')
    []
    """
    import re

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    '''
    if 标识自动转义:
        for i in ".*?()[]":
            if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
            if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
            # front = re.sub('[%s]' % i, "\\" + i, front)
            # behind = re.sub('[%s]' % i, "\\" + i, behind)
            # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
    '''

    for i in ".*?()[]":  # TODO 可能还有问题 因为元字符 还包括 + - \ ^ { } 等等
        # front = front.replace(i, "\\" + i)
        # behind = behind.replace(i, "\\" + i)
        if i in front:
            front = front.replace(i, "\\" + i)
        if i in behind:
            behind = behind.replace(i, "\\" + i)
        # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错

    # re.S 表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
    return re.findall(front + '(.*?)' + behind, string, re.S)


def 文本_是否包含字母(string):
    for i in string:
        # if '\u0030' <= i <= '\u0039':
        if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
            return True
    # 循环完毕 都还没返回 那结果就是False了
    return False


def 文本_是否全为字母(string):  #
    for i in string:
        # if (not '\u0061' <= i <= '\u007a') or (not '\u0041' <= i <= '\u005a'):
        # if (not 'a' <= i <= 'z') or (not 'A' <= i <= 'Z'):
        '''以上的逻辑写错了'''
        '''正确的逻辑:  不在 小写字母的区间 且 不在 大写字母的区间 '''
        ''' '''
        if (not 'a' <= i <= 'z') and (not 'A' <= i <= 'Z'):
            return False
        # if (('a' <= i <= 'z') == False) and (('A' <= i <= 'Z') == False): return False
    # 循环完毕 都还没返回 那结果就是True了
    return True


# 检验是否含有中文字符
def 文本_是否包含汉字(string):
    """
    >>> 文本_是否包含汉字('123ni你好asasa')
    True
    >>> 文本_是否包含汉字('123niasasa')
    False
    >>> 文本_是否包含汉字('123')
    False
    >>> 文本_是否包含汉字('a')
    False
    >>> 文本_是否包含汉字('你')
    True
    >>> 文本_是否包含汉字('1')
    False
    """
    for i in string:
        if '\u4e00' <= i <= '\u9fa5':
            # if '一' <= i <= '龥':
            return True
    # 循环完毕 都还没返回 那结果就是False了
    return False


# 检验是否全是中文字符
def 文本_是否全为汉字(string):
    for i in string:
        if not '\u4e00' <= i <= '\u9fa5':
            return False
    # 循环完毕 都还没返回 那结果就是True了
    return True


def 文本_取汉字(string):
    # 返回:列表  空列表[]  或者 有数据的列表
    # Failed example:    文本_取汉字('能取group取值')
    # Expected:    ['能取','取值']
    # Got: ['能取', '取值']
    #     >>> if None:print('代码示例:')
    """
    >>> 文本_取汉字('你好gro哈哈up呵呵')
    ['你好', '哈哈', '呵呵']
    >>> 文本_取汉字('123aaaa121212')   #测试
    []
    >>> 文本_取汉字('你123a你好吗aaa文本')
    ['你', '你好吗', '文本']
    >>> 文本_取汉字('1')
    []
    >>> 文本_取汉字('a')
    []
    """
    import re
    # return re.compile("[\u4e00-\u9fa5]").findall(文本)
    return re.compile("[\u4e00-\u9fa5]+").findall(string)  # 备注:这种是返回列表  并且没有re.S注释掉换行符
    # search的问题:需要对re.search返回的对象进行判断,不是None才能取group取值.
    # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
    # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
    # return re.search("[\u4e00-\u9fa5]+",string,re.S).group()   #这种是返回单条数据对象 并且注释掉换行符 要对其对象是否None判断后 再对其group取值


def 文本_取英文数字(string):
    # 返回: 列表  空列表[]  或者 有数据的列表
    import re
    return re.compile("[a-zA-Z0-9]+").findall(string)  # 连在一起的会一起加入列表  #没有+号 会返回1个个的匹配对象


def 文本_取数字(string):
    # 返回列表  空列表[]  或者 有数据的列表
    """
    >>> 文本_取数字('00abbbb12你3334好013549abcde')
    ['00', '12', '3334', '013549']
    >>> 文本_取数字('accva')
    []
    """
    import re
    # return re.compile("[0-9]").findall(文本)  #这种会返回1个个的数字
    return re.compile("[0-9]+").findall(string)  # 连在一起的数字会一起加入列表  #可行
    # return re.compile("\d+").findall(string)  #连在一起的数字会一起加入列表 #这个也行  \d和\\d都可以


def 文件_图片写到文件(file, data):
    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    # 多用于 图片字节集 写到本地图片
    with open(file, "wb") as f:
        f.write(data)


def 文本_到字典(text: str):  # 用来取postdata
    li = text.split("&")
    dic = {}
    for i in li:
        # temp_li=i.split("=")
        k, v = i.split("=")
        dic[k] = v
    return dic


def 文本_遍历(string):
    """
    >>> string = 'ABCDEF'
    >>> for i in string:print(i)
    A
    B
    C
    D
    E
    F
    """

    for i in string:
        print(i)

    # for 循环 遍历
    # for i in str:
    #     print(i)
    # A
    # B
    # C
    # D
    # E
    # F


def 文本_取单个字符(string, index):  # 文本是N个字符组成的数组
    return string[index]
    # str = 'ABCDEF'
    # print(str[0])  #A


def 文本_修改():
    # 只能用下面类似format方法  不能像数组那样用索引改
    # python中字符串属于不可改变对象，不支持原地修改，如果需要修改其中的值，只能重新创建一个新的字符串对象。 比如format之类
    # s2[2] = 'c'  # TypeError: 'str' object does not support item assignment
    return None


def 文本_替换_format方法():
    # 二、format   ★{}作为占位符 format引出  占位符如果要填索引或者关键字就在{}里面填
    # 三种方式:
    # 第一种:按顺序接收参数
    s1 = '我叫{},今年{}，性别{}'.format('小明', '18', '男')
    print(s1)  # 我叫小明,今年18，性别男

    # 第二种:按索引接收参数
    s2 = '我叫{0},今年{1}，性别{2}，我依然叫{0}'.format('小明', '18', '男')
    print(s2)  # 我叫小明,今年18，性别男，我依然叫帅哥

    # 第三种：按关键字接收参数
    s3 = '我叫{name},今年{age}，性别{sex}'.format(age='18', name='小明', sex='男')
    print(s3)  # 我叫小明,今年18，性别男


def test_文本_子文本替换():
    string = "1234561234"

    print(string.replace('2', 'b'))  # 1b34561b34  #全部替换
    print(string.replace('2', 'b', 1))  # 1b34561234  # 只替换1次
    print(string)  # 1234561234  # 原本的string不会被改变 需要用变量接收

    print(文本_子文本替换(string, '2', 'b'))  # 1b34561b34
    print(文本_子文本替换(string, '2', 'b', 1))  # 1b34561234
    print(string)  # 1234561234

    assert 1 == 1


def 文本_替换(string, old, new, *count):  # 同:文本_子文本替换
    """
    :param string:
    :param old:
    :param new:
    :param count:  替换次数 可省略
    :return:
    """
    # str = 'ABCDEF'
    # print(str.replace('C','G'))  #ABGDEF
    return string.replace(old, new, *count)  # replace 不会改变原 string 的内容。 需要接收方 接收新的值


def 文本_子文本替换(string, old, new, *count):
    # string=''
    return string.replace(old, new, *count)  # replace 不会改变原 string 的内容。 需要接收方 接收新的值


def 文本_分割(string, 分隔符):
    """
    分割文本,返回数组,比如'ABCDEF' 分隔符为'D' 返回 ['ABC', 'EF']
    如果分隔符并不存在 会作为1整个元素返回   比如:str.split('qq'))  # ['abcdef']
    :param string:
    :param 分隔符:
    :return:
    """
    # str = 'ABCDEF'
    # print(str.split('D'))  # ['ABC', 'EF']
    return string.split(分隔符)

    # 文本-->数组  分割 str.split(分割符)
    # print(str.split('b'))  # ['a', 'cdef']
    # print(str.split('qq'))  # ['abcdef']


def 字典_到文本(dic: dict):
    li = []
    for k, v in dic.items():
        li.append(k + "=" + v)
    return "&".join(li)


def 文本_是否_():
    # ■ ★原生 有点问题
    # str = 'ABCDEF'
    # print(str.isalpha()) # True
    # print(str.isalnum()) # True
    # print(str.isdigit()) # False

    # ■★python 自带语句的bug:digit 甚至包含全角中文  numeric 甚至包含汉字数字 比如一二..十 甚至包含财务数字 壹贰 alnum 甚至包含汉字 我靠 原因是alpha就包含汉字
    # ■★python 特性:字符串与字符串间的大小比较 是按unicode编码来比较的 所以可以直接比较.
    # 1.通过ord()转为acsii码数字再比的,就多一道东西了,不需要
    # 2.直接写unicode字符 比如if '\u0030' <= i <= '\u0039' 比较麻烦 本质还是比较unicode编码
    # 3.直接写str起始字符 就最简单了 比如:if '0' <= i <= '9':pass  if  'a' <= i <= 'z':pass   if 'A' <= i <= 'Z':pass
    # 但是汉字的话  '\u4e00' <= i <= '\u9fa5'  '一' <= i <= '龥':  龥(yu4)写起来麻烦
    # 还是记一下范围 \u4e00 ~ \u9fa5  正则也用得到

    pass


def 文本_是否包含数字(string):
    for i in string:
        # if '\u0030' <= i <= '\u0039':
        if '0' <= i <= '9':
            return True
    # 循环完毕 都还没返回 那结果就是False了
    return False


def 文本_是否全为数字(string):  # 小数点 也不能算 全为数字
    for i in string:
        # 0 -9 的 unicode编码   就是ascii码转为16进制
        """ unicode编码 比较"""
        # if not '\u0030' <= i <= '\u0039':
        """ ascii编码 比较"""
        # print(ord(i))
        # if not ord('0') <= ord(i) <= ord('9'):
        """ unicode编码 比较 """  # 另一种形式的比较:str的比较, 按unicode 编码比较每个字符的大小
        if not '0' <= i <= '9':
            return False
    # 循环完毕 都还没返回 那结果就是True了
    return True


def 文本_到bytes(string):
    return string.encode()
    # print("中文".encode())  # 这个也行    #string.encode()
    # print(b'\xe4\xb8\xad\xe6\x96\x87'.decode())  # bytes.decode()


def bytes_到文本(bytes_):
    # b'\xe4\xb8\xad\xe6\x96\x87'.decode()
    return bytes_.decode()


if __name__ == '__main__':
    _dict = 文件_取出字典('dict.txt')
    print(_dict)
    字典_写到文件(_dict, 'dict.txt')
