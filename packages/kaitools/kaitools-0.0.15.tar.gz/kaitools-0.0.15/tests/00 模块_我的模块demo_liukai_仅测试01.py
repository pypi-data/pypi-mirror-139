import pathlib
import os

print('成功导入我的demo', 'liukai.py')

'''
def 时间_到文本(包含时分秒=False):
    import time
    t = time.localtime()
    # print(t)
    # tm_hour  tm_min   tm_sec
    if 包含时分秒:
        return(
                str(t.tm_year) + "年" +
                str(t.tm_mon) + "月" +
                str(t.tm_mday) + "日"+
                str(t.tm_hour) + "时" +
                str(t.tm_min) + "分" +
                str(t.tm_sec) + "秒"
        )
    else:
        return (
            str(t.tm_year) + "年" +
            str(t.tm_mon) + "月" +
            str(t.tm_mday) + "日"
        )



def 时间_取现行时间戳():  # 这个写13位
    import time
    return (int(round(time.time() * 1000)))
    # return int(round(time.time() * 1000))   #return (x) 可以不加括号


# 文本_读入文本   #一.文件不存在   二.文件编码是gb2312? /文件编码是utf8?
def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()
'''

print(bool([]), '[]')
print(bool([1]), '[1]')
print(bool(0), 0)
print(bool(1), 1)
print(bool(""), '\"\"')
print(bool("1"), '1')


def 文件_是否存在(filename):
    import pathlib
    # path = pathlib.Path(file)
    return pathlib.Path(filename).is_file()


def 文件_更名(file_oldname, file_newname):
    import os
    os.rename(file_oldname, file_newname)


file = r"D:\1\3"
# 文件_是否存在


print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行

print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
