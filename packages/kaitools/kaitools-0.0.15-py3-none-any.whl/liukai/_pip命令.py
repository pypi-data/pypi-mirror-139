r"""

# "pip命令.md" 文件

# 加快下载包的速度
# pip install + 包名 + （去掉加号，包名为需要的包名） -i https://pypi.tuna.tsinghua.edu.cn/simple
× pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pypiwin32 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装requirements.txt
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
' --------------------------+----------------------------
卸载
pip uninstall pywin32
' --------------------------+----------------------------
pip命令   在终端


## 生成依赖文件txt

```
pip freeze>requirements.txt
```



## 安装依赖文件txt

```python
pip install -r requirements.txt
```



pip 应该是大家最熟悉的 Python 包安装与管理工具了，但是除了pip install 这个最常用的命令，还有很多有用的玩法。这里就介绍几个我平时会用到的，希望对大家有所帮助。

## pip freeze

这个命令可以查看已经安装的包及版本信息，当你要换电脑，或者朋友想复刻你已安装的包，又不想一个一个重新安装。这时就可以使用pip freeze > requirements.txt ，批量导出当前开发环境的包信息，然后安装requirements.txt依赖就行了。

```
pip freeze > requirements.txt
pip install -r requirements.txt
```

## pip cache

用pip安装python模块的时候，重复安装某一模块会经常出现“Using cache”，这样很容易装错版本。而且cache还会占用不少C盘空间，如果空间不足，可以直接删除这些缓存。 方法：

Win + R ，输入%LocalAppData%\pip\Cache

删掉 cache/ 目录下的所有文件夹就好了

## pip list

pip list 命令列出所有安装包和版本信息，pip list --outdate可以列出所有可升级的包。

![图片](https://mmbiz.qpic.cn/mmbiz_png/njjfaJS7c9rkjwHLxfSazd9VyJx2ibepDcXJmz2U6NUXs9eUhJYd19ibun1XEtTWEo5Isce9PrmRrVxPb8rJf3kw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)但是当前内建命令并不支持升级所有已安装的Python模块，不过可以写一个：

```
import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions
for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
```

替代方案是使用pip-review，这是一个分叉pip-tools，升级包就太方便了。安装和使用方法：

```
pip install pip-review
#查看可更新
pip-review
#自动批量升级
pip-review --auto
#以交互方式运行，对每个包进行升级
pip-review --interactive
```

## pip.init

pip 用国外的源下载安装包会比较慢，还经常出错安装失败，可以将安装源切换成国内镜像，速度×10！改一些pip.init配置，一劳永逸，具体做法：Win + R ，输入  %APPDATA% 在当前目录下新建 pip 文件夹，然后新建 pip.ini 文件，内容如下

```
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/trusted-host=mirrors.aliyun.com
```

我直接设置成了阿里的,豆瓣的源速度也很快。

```
豆瓣(douban) http://pypi.douban.com/simple/
清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/



"""