import win32gui
import win32con
import win32api


# import win32com
# import win32ui

# 问题: pip install pywin32  --> 改为 pip install pypiwin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
# windows系统上出现这个问题的解决需要安装Py32Win模块，但是直接通过官网链接装exe会出现几百个错误，更方便的做法是
# Scrapy运行ImportError: No module named win32api错误

def 系统_取桌面分辨率():
    import ctypes
    winapi = ctypes.windll.user32
    x = winapi.GetSystemMetrics(0)
    y = winapi.GetSystemMetrics(1)
    print(x)
    print(y)
    # 1440
    # 900
    return x, y


def 信息框(msg="信息提示", title="窗口标题"):
    # 示例: 弹窗("my warning~!提示!")
    import ctypes
    ctypes.windll.user32.MessageBoxA(0, msg.encode('gb2312'), title.encode('gb2312'), 0)
    # ctypes.windll.user32.MessageBoxA(0,msg.encode('utf-8'),title.encode('utf-8'),0) #★utf-8也会乱码
    # ctypes.windll.user32.MessageBoxA(0,msg,title,0) #★原始位置只接受bytes 不编码就有问题
    # ctypes.windll.user32.MessageBoxA(0,u"点击确定 开始处理data目录下面的xls文件,分析处理完成后会有提示.^_ ^".encode('gb2312'),u' 信息'.encode('gb2312'),0)


def 注册表_强制刷新():
    # 可以强制注册表生效 比如改完注册表后的环境变量
    import ctypes

    # 方式1 有时候会卡住 遇到过刷新注册表卡住 不结束
    # ctypes.windll.user32.SendMessageW(65535, 26, 0, "Environment")  # -->可以刷新注册表
    # ctypes.windll. 到这里就没智能提醒了

    # 方式2:
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
    SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))

    # 写法2:
    # c = ctypes.WinDLL("user32.dll")
    # c.SendMessageW(65535, 26, 0, "Environment")

    # 历史笔记:
    # ctypes.windll.user32.SendMessage(65535, 26, 0, "Environment")  #-->无效 没有这个方法 AttributeError: function 'SendMessage' not found
    # 百度 SendMessage  发现 是分为 SendMessageA SendMessageW
    # 然后google搜索 "ctypes.windll.user32.SendMessage" 看到类似 SendMessage = ctypes.windll.user32.SendMessageW
    # ctypes.windll.user32.SendMessageA(65535, 26, 0, "Environment")  #-->无效  不会报错 但是也无法刷新注册表
    # ■ctypes.windll.user32.SendMessageW(65535, 26, 0, "Environment")  # -->可以刷新注册表

    # 历史:方法: 需要win32gui win32api win32con 那些东西 很麻烦
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Environment")


# logging 模块 打包一个方法
def loggerNew_____(filename=None, 输出到屏幕=True):  # ■□这种不是单例模式  2020年11月写了个单例模式的 在模块liukai_single_log
    # def _logger(filename=None, 输出到屏幕=True):
    """用法示例:
    #1.获取一个初始化对象:
        logger = _logger()    #默认  :日志路径:./MyLog/Log 文件
        logger = _logger(输出到屏幕=False)  #这种就不会输出到屏幕上 只会写日志
        logger = _logger(filename="my_test_logging")  #这种日志路径./MyLog/my_test_logging文件
    #2.调用:
        logger.warning("开始...")
        logger.info("提示")
        logger.error("错误")
        logger.debug("查错")
    """
    import os
    import logging.handlers
    #    from logging import handlers

    # 初始赋值:filename
    if filename is None:
        filename = 'Log'

    # 创建log对象
    logger = logging.getLogger(filename)  # logger = logging.getLogger()也可以 对应的是Formatter里面的name
    # 设置日志等级
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.ERROR)
    # 日志格式
    formatter = logging.Formatter('%(asctime)s - [%(filename)s] - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
    # formatter = logging.Formatter('[%(asctime)s] - [%(filename)s] - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
    # formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
    # formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(filename)s %(message)s", datefmt="%Y/%m/%d %X")
    # 创建:写日志文件的句柄
    os.makedirs("./MyLog/", exist_ok=True)  # 创建文件夹
    fh = logging.handlers.TimedRotatingFileHandler(filename="./MyLog/" + filename, when='MIDNIGHT', interval=1,
                                                   backupCount=0, encoding="utf-8")
    # 设置滚动日志的后缀
    fh.suffix = "%Y-%m-%d.log"
    # 绑定日志格式到句柄
    fh.setFormatter(formatter)
    # 每个句柄单独设置级别
    # fh.setLevel(logging.DEBUG)
    # 句柄 添加到logger对象
    logger.addHandler(fh)

    """判断是否输出到屏幕"""  # 创建输出到屏幕句柄
    if 输出到屏幕:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        # ch.setLevel(logging.DEBUG)  #每个句柄单独设置级别
        logger.addHandler(ch)

    return logger


# 窗口_置顶
def 窗口_置顶(hwnd):
    # import win32gui
    """可行方案 demo"""
    # 1.最小化  #2.被遮挡  #2种情况下 能置顶显示

    # 如果是最小化:https://blog.csdn.net/qq_16234613/article/details/79155632
    if win32gui.IsIconic(hwnd):
        # print("检测,最小化")
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)  # 4 最小化用这个恢复 可以 #被遮挡不行
        win32gui.ShowWindow(hwnd, 4)  # 4 最小化用这个恢复 可以 #被遮挡不行
    else:
        # print("检测,not最小化")
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # 8 被遮挡 用这个恢复 可以 #最小化不行
        win32gui.ShowWindow(hwnd, 8)  # 8 被遮挡 用这个恢复 可以 #最小化不行

    from win32com.client import Dispatch
    Dispatch("WScript.Shell").SendKeys('%')  # 为了解决win32gui.SetForegroundWindow(hwnd)的bug
    win32gui.SetForegroundWindow(hwnd)  # 置前显示


# 枚举窗口hwnd_list的代码:
def 窗口_枚举():
    # import win32gui
    # 返回 hwndList
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    # print(hWndList)
    return hWndList


# 窗口_查找窗口_支持模糊类名和标题
def 窗口_FindWindow_模糊(classname="", title=""):
    # import win32gui
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    # print(hWndList)
    for hwnd in hWndList:
        t = win32gui.GetWindowText(hwnd)
        c = win32gui.GetClassName(hwnd)
        # print(t, c)
        if (title in t) and (classname in c):
            # print(t, c)
            # print("t, title", t, title)
            return hwnd
    return None


# 窗口_查找窗口
def 窗口_FindWindow(classname, title):
    # import win32gui
    # hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", "Appium")
    # hwnd = win32gui.FindWindow(classname, title)
    return win32gui.FindWindow(classname, title)


def 窗口_取子窗口句柄(父hwnd, 子窗口类名):
    # import win32gui
    # win32gui.FindWindowEx()
    # https://blog.csdn.net/seele52/article/details/17504925
    # https://segmentfault.com/q/1010000004506806
    # hWnd = win32.user32.FindWindowW('Notepad', None)
    # hEdit = win32.user32.FindWindowExW(hWnd, None, 'Edit', None)

    # 获取父句柄hwnd类名为clsname的子句柄
    # hwnd1 = win32gui.FindWindowEx(hwnd, None, clsname, None)

    return win32gui.FindWindowEx(父hwnd, None, 子窗口类名, None)


# 获得当前鼠标位置
def 窗口_取鼠标位置():
    # def get_curpos():
    # (37, 607)  元组方式
    # import win32gui
    return win32gui.GetCursorPos()


# 获得指定位置窗口句柄：
def 窗口_取句柄_指定位置(pos):
    # def get_win_handle(pos):
    # import win32gui
    return win32gui.WindowFromPoint(pos)


def 窗口_取句柄_GetMousePointWindow():
    # def 窗口_取句柄_鼠标指向位置():
    # import win32gui
    return win32gui.WindowFromPoint(win32gui.GetCursorPos())


def 窗口_关闭(hwnd):
    # import win32gui
    # import win32con
    # win32gui.PostMessage(win32lib.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
    # win32gui.PostMessage(win32gui.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def 窗口_取屏幕句柄():
    # import win32gui
    return win32gui.GetDesktopWindow()


def 窗口_取标题(hwnd):
    # import win32gui
    return win32gui.GetWindowText(hwnd)


def 窗口_取类名(hwnd):
    # import win32gui
    return win32gui.GetClassName(hwnd)


def 窗口_是否最小化(hwnd):
    # 非最小化:0被遮挡,前台  最小化1
    # import win32gui
    return win32gui.IsIconic(hwnd)


def 窗口_GetClientRect(hwnd):
    # (0, 0, 371, 863)         0,0,宽度,高度
    # import win32gui
    return win32gui.GetClientRect(hwnd)


def 窗口_GetWindowRect(hwnd):
    # #(335, 0, 706, 863)    x1,y1,x2,y2  窗口坐标系
    # import win32gui
    return win32gui.GetWindowRect(hwnd)
    # def 窗口_GetWindowRect(hwnd):
    #     import win32gui
    #     rect = win32gui.GetWindowRect(hwnd)
    #     return rect[0], rect[1]


def 窗口_句柄_取进程ID(hwnd):
    import win32process  # 进程模块
    hid, pid = win32process.GetWindowThreadProcessId(hwnd)
    # hid是线程id吗??
    return pid


def 鼠标_moveto(*args):  # 优势:支持 鼠标_moveto(x, y) 也支持鼠标_moveto((x,y))格式
    # def 鼠标_moveto(x, y):
    # import win32api
    # win32api.SetCursorPos([x, y])  #函数原型
    # print(*args)
    # print(args)
    # print(len(args)) #这个没问题  2个参数就是args=(1, 2) len就是2 1个元组就是1
    # print(len(*args))  #报错 会因为参数问题  *args是解包 解包后的2个int 是不能被len的
    """
    笔记:关于传入参数是否解包的问题:
    比如传入2个参数x,y    def *args 实际用的时候 args就是原样x,y传入
    比如传入1个参数(x,y)  def *args 实际用的时候 *args就是解包 (x,y)解包为x,y
    另外:len(args) 就是args里面参数的个数,x,y就2个,(x,y)就1个 
    """
    if len(args) == 1:
        # win32api.SetCursorPos(list(*args))  ##这种可以鼠标_moveto((1,2))
        win32api.SetCursorPos(*args)  # 这种可以鼠标_moveto((1,2))
    if len(args) == 2:
        win32api.SetCursorPos(args)  # 这种可以 鼠标_moveto(1,2)


# print(*args[0],*args[1]) #错误 TypeError: print() argument after * must be an iterable, not int
# win32api.SetCursorPos([*args]) #不解包的话,有一个会报错
# win32api.SetCursorPos([args])
# x,y=args
# lis=list(*args)     #这种可以鼠标_moveto((1,2))  #这种不行 鼠标_moveto(1,2)
# win32api.SetCursorPos(lis)
# win32api.SetCursorPos([x, y])

def 鼠标_LeftClick_X_Y(*args):
    # 鼠标_点击坐标(102,637)
    # 鼠标_点击坐标((102,637))
    # import win32api
    # import win32con
    # if isinstance(args,tuple):
    #     x, y = *args[0], *args[1]
    x, y = None, None
    if len(args) == 1:
        x, y = *args[0], *args[1]
        # win32api.SetCursorPos(*args)  #这种可以鼠标_moveto((1,2))
    if len(args) == 2:
        x, y = args
        # win32api.SetCursorPos(args)  #这种可以 鼠标_moveto(1,2)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    '''原型
    def click1(x,y):                #第一种  #前台
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    #原文链接：https://blog.csdn.net/qq_16234613/article/details/79155632
    '''


def _鼠标_LeftDown():
    # 左键 按下
    # import win32api
    # import win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # ; // 点下左键


def _鼠标_LeftUp():
    # 左键 弹起
    # import win32api
    # import win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # ; // 点下左键


def _鼠标_RightDown():
    # 右键 按下
    # import win32api
    # import win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  # ; // 点下左键


def _鼠标_RightUp():
    # 右键 弹起
    # import win32api
    # import win32con
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# 支持 左键/右键 + 单击/按下/放开
def 鼠标_按键(键=0, 按键类型=0):
    """
    # 支持 左键/右键 + 单击/按下/放开
    # 键 左键0 右键1
    # 按键类型 默认为0 单击；1 #按下 2 #放开
    """
    # import win32api
    # import win32con

    if 键 == 0:
        if 按键类型 == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  #
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  #
        elif 按键类型 == 1:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  #
        elif 按键类型 == 2:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  #
    if 键 == 1:
        if 按键类型 == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  #
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif 按键类型 == 1:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  #
        elif 按键类型 == 2:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# 默认为0 单击；1 #按下 2 #放开
def 键盘_按键(键代码, 按键类型=0):
    # 默认为0 单击；1 #按下   2 #放开
    # 键代码 可以去win32con里面的VK_部分找  也可以在网上直接找虚拟键码表
    # import win32api
    # import win32con

    # if type(键代码) == type(1): pass
    if isinstance(键代码, int):
        pass
    # if type(键代码) == type("1"):
    if isinstance(键代码, str):
        # tod1 需要转换为键代码
        # tod2 小写字母要转换为大写字母 再ord取键代码 只支持小写字符
        键代码 = 键代码.upper()
        键代码 = ord(键代码)

    if 按键类型 == 0:
        win32api.keybd_event(键代码, 0, 0, 0)  # Delete
        win32api.keybd_event(键代码, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    elif 按键类型 == 1:
        win32api.keybd_event(键代码, 0, 0, 0)
    elif 按键类型 == 2:
        win32api.keybd_event(键代码, 0, win32con.KEYEVENTF_KEYUP, 0)


def 键盘_组合按键(*args):
    """
    *args 需要为键码数字  文本方式目前只支持"大写/小写"单个字母
    示例1:键盘_组合按键(win32con.VK_LCONTROL, win32con.VK_MENU,"s")
    示例1:键盘_组合按键(17,18,83)  #这里83是大写S的键码 小写的不能用与其它功能键重复
    # 支持键码数字或者wincon常量
    # 兼容大小写字母 比如ctrl+alt+s 和 ctrl+alt+S一致
    """
    # import win32api
    import win32con

    # todo  没写完  #准备把
    dic = {"ctrl": win32con.VK_LCONTROL,
           "alt": win32con.VK_MENU,
           "shift": win32con.VK_SHIFT,
           "win": win32con.VK_LWIN
           }
    print(dic)
    lis = list(args)
    print(lis)
    # ★对字母的处理 小写字母要转换成大写字母对应的键码
    for i in range(len(lis)):
        # print(lis[i])

        # done 关于数字的处理
        # if type(lis[i]) == type("文本"):

        if isinstance(lis[i], str):  # if type("文本") == type(lis[i]):
            lis[i] = lis[i].upper()  # 变大写
            lis[i] = ord(lis[i])  # 取得键码数字
            # print(lis[i])
        # todo 这里要处理 文本长度是否异常
        # todo 这里要处理是否都是键码
        if type(lis[i]) is not int:
            print("检测到非数字键码,异常")
            return
    for i in lis:
        win32api.keybd_event(i, 0, 0, 0)  # 按下键码
        print()
        # todo 这里可以检测按键状态,调试输出
    for i in lis:
        win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)  # 弹起键码
        # todo 这里可以检测按键状态,调试输出


def 鼠标_消息(): pass


def 键盘_消息(hwnd, 键代码, 状态=0, 是否功能键=False):
    # 作用:发送 后台按键
    # 状态  0=输入字符(大写) 1=输入字符(小写)  2=按下，3=放开，4=单击
    # 是否功能键  默认为假：普通键   真:功能键 (为功能键可用于热键技能不输入字符)
    # import win32gui
    if 是否功能键 is True:
        # WM_SYSKEYDOWN = 260
        # WM_SYSKEYUP = 261
        按下 = 260
        放开 = 261
    else:
        # WM_KEYDOWN = 256
        # WM_KEYUP = 257
        按下 = 256
        放开 = 257
    if 状态 == 0:
        # WM_CHAR = 258
        win32gui.PostMessage(hwnd, 258, 键代码, 0)
    if 状态 == 1:
        win32gui.PostMessage(hwnd, 按下, 键代码, 0)
    if 状态 == 2:
        win32gui.PostMessage(hwnd, 按下, 键代码, 0)
    if 状态 == 3:
        win32gui.PostMessage(hwnd, 放开, 键代码, 0)
    if 状态 == 4:
        win32gui.PostMessage(hwnd, 按下, 键代码, 0)


def adb_tap(x, y, delay=0.5):
    # 用来 运行 点击屏幕坐标命令  driver.tap()点击无效
    import os
    import time
    # dx, dy = 544, 1346
    # os.popen("adb shell input tap " + str(x) + " " + str(y))
    cmd = "adb shell input tap {x} {y}".format(x=x, y=y)  # 不用转换为str 默认就转换了好像
    # os.popen("adb shell input tap " + str(x) + " " + str(y))
    os.popen(cmd)
    time.sleep(delay)


# print("时间_取现行时间戳", 时间_取现行时间戳)

"""测试耗时:"""
# import time

# print(time.ctime(), '代码起始时间')

# print(res)

# print(time.ctime(), '代码结束时间')

"""测试耗时:"""
# import time

# t = time.time()

# print('代码开始,计时' , t )

# print(do something....)

# print( '代码结束.耗时:' , time.time()-t)


if __name__ == '__main__':
    import doctest

    # doctest.testmod(verbose=True)
    doctest.testmod()
