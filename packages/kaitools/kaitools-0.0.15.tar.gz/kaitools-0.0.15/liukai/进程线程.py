import os

from liukai.文件文本 import 文本_取中间_批量


def 进程_结束(process_name):
    # def process_kill(process_name):
    # cmd = 'taskkill /f /im wuauclt.exe'  # 代码原型:
    # os.system('taskkill /f /im wuauclt.exe')
    if not process_name.endswith(".exe"):
        process_name += ".exe"
    cmd = 'taskkill /f /im {}'.format(process_name)
    with os.popen(cmd) as f:
        print(f.read())


def tasklist_fi(process_name="闹钟_by雪天"):
    """根据指定的进程名称  输出 列表 """

    # cmd = 'tasklist /fi "imagename eq java.exe"'  # 信息: 没有运行的任务匹配指定标准。

    # cmd = 'tasklist /fi "imagename eq iexplore.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe" /FO LIST'  # 信息格式 输出为LIST
    '''默认table 格式
    映像名称                       PID 会话名              会话#       内存使用
    ========================= ======== ================ =========== ============
    iexplore.exe                 24364 Console                    1     33,864 K
    iexplore.exe                 11700 Console                    1    124,116 K
    '''
    if not process_name.endswith(".exe"):
        process_name += ".exe"

    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)

    with os.popen(cmd) as f:
        r = f.read()
        # print(f.read())
    print(r)
    # --> demo
    return r


def 进程_取pid(process_name="iexplore"):
    """
    参数:进程名称
    作用:取出全部pid
    返回值:list 文本型  ['20068', '22776']   如果没有这个进程 就是 []
    """
    # def process_pid(process_name="闹钟_by雪天"):
    # cmd = 'tasklist /fi "imagename eq java.exe"'  # 信息: 没有运行的任务匹配指定标准。

    # cmd = 'tasklist /fi "imagename eq iexplore.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe" /FO LIST'  # 信息格式 输出为LIST
    '''默认table 格式
    映像名称                       PID 会话名              会话#       内存使用
    ========================= ======== ================ =========== ============
    iexplore.exe                 24364 Console                    1     33,864 K
    iexplore.exe                 11700 Console                    1    124,116 K
    '''
    if not process_name.endswith(".exe"):
        process_name += ".exe"

    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)

    with os.popen(cmd) as f:
        r = f.read()
        # print(f.read())
    # print(r)
    # return r  --> demo  #■ 到这里为止 就是输出信息了  下面要取pid列表

    # r_list= r.split("\n")
    # print(r_list)
    # for i in r_list:
    # for i in range(len(r_list)):
    # if process_name in r_list[i]:
    #     print(r_list[i])
    # for n in r_list[i]:
    #     print(ord(n))  # 调试 发现 :中间的是 空格符
    # print(r_list[i].encode(b))  -->错误
    # print(bytes(r_list[i], encoding="utf-8"))  --> 错 不是想要的unicode字符

    # ■■这里
    # 1.正则可以取  process_name[\s]+([0-9]*)[\s]+
    # 2.文本 批量取中间 也可以  取完要去掉空格字符
    # ■□发现 其实csv格式的更好批量取文本 CSV是这种 "iexplore.exe","16004","Console","1","33,140 K" 前面文本exe"," 后面文本"
    lis = 文本_取中间_批量(r, process_name, "Console")
    for i in range(len(lis)):
        lis[i] = lis[i].strip()  #

    return lis


# 线程_启动  线程方式运行 子程序
def thread_it(func, *args, **kwargs):
    import threading
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    return t


def _async_raise(tid, exctype):
    import ctypes
    import inspect
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# 线程_停止
def thread_stop(thread):
    _async_raise(thread.ident, SystemExit)

