import execjs  # pip install PyExecJS
import os

# ★ js计算()  '09 python_执行js语句_execjs_0笔记demo.py'
# ★ 因为安装了node.js 所以目前引擎默认是Node.js (V8),有部分js使用Node.js (V8)会报错,异常.因此出现异常则切换到JScript.使用完毕就切换回来Node.js (V8)
# ★ 至于为什么不直接使用JScript,是因为JScript有时候计算的特别慢.
from liukai.文件文本 import 文件_读入文本


def js计算(file, *args):
    # 格式:js计算(js文件路径,js中func名称,func要用的参数)
    # 示例1:js计算('js_2.js','get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')      #js文件 相对路径 就在本目录下
    # 示例2:js计算(r'c:\js_2.js','get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')  #js文件完整路径
    """
    简化成一句话代码:
    """
    # print('args',args)
    # print('*args', *args)   # 我的 笔记 :*的作用:uppack  如果不加* 那传进来就是个tuple
    defult = execjs.get().name  # 取默认js环境  #原因:这里面改到JScript默认就一直是了 不会换回默认环境 因此在切换后 最好置回默认环境
    # 当然 也可以只使用JScript环境

    file = 文件_读入文本(file)  # ★这个有自动适配gb2312或者utf-8
    # with open(file, mode="r", encoding='utf-8') as f:
    #     file = f.read()

    try:
        # res = execjs.compile(open('js_2.js', 'r', encoding='utf8').read()).call('get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')
        print(execjs.get().name, '默认js')
        res = execjs.compile(file).call(*args)
        # res = execjs.compile(file).call(args,)
        # 我的笔记:这种就是错误的写法 原因是没有*,会传入tuple,而非单独的每个参数
    except:  # except:
        print(execjs.get().name, '检测到默认js存在问题,已切换至JScript')
        os.environ["EXECJS_RUNTIME"] = "JScript"
        res = execjs.compile(file).call(*args)
        os.environ["EXECJS_RUNTIME"] = defult  # 置回默认js环境

    return res

