# 官方文档:https://docs.python.org/3/library/configparser.html

import configparser


def ini_read(file, section, option):
    config = configparser.ConfigParser()  # 初始化一个对象configparser
    config.read(file, encoding='utf-8-sig')  # ★utf-8-sig解决中文存储和读取的问题  utf-8不行

    # 2.判断option 是否存在
    if not config.has_option(section, option):
        print("option不存在", option)
        return None

    # 3.返回读取到的 value
    return config.get(section, option)

    # return config[section][option]  ★等同 config.get(section, option) 参考了官方文档:https://docs.python.org/3/library/configparser.html


def ini_write(file, section, option, value):
    config = configparser.ConfigParser()  # 初始化一个对象configparser

    config.read(file, encoding='utf-8-sig')  # ★是的 修改也要先读 类似文件open read write的原理 就理解成它必须读到原有文件 搞到缓冲池里 所有修改都是在缓冲池进行 最后写到文件生效

    if not config.has_section(section):
        config.add_section(section)  # 添加section

    config.set(section, option, value)  # 设置值  #2.要判断option是否存在?-->★测试结论:不需要 不影响 #设置值.如果是空值或者有值,会覆盖原有

    # 这里为了防止误写入 修改了原有ini 可以先备份1次 .时间戳.bak  再进行后面的写入
    with open(file, "w", encoding='utf-8-sig') as f:
        config.write(f)  # 这个模块独有的write方法,和常规的文件读写有点区别


def ini_遍历(file):
    config = configparser.ConfigParser()  # 初始化一个对象configparser
    config.read(file, encoding='utf-8-sig')  # 这里必须要read 无论是后面read还是write
    print(config.sections())
    for i in config.sections():
        print("当前section:", i)
        print("开始遍历 option", config.options(i))  # 得到该section的所有option
        # print (config.items(i)   ,'config.sections 开始取值 遍历 items 形成option:value键值对')  #[('option1', 'v1'), ('k2', 'v2'), ('中文', 'v333')]
        for n in config.options(i):
            # i 是 当前section   n是当前option的value
            print('option:', n, 'value:', config.get(i, n))  # [('option1', 'v1'), ('k2', 'v2'), ('中文', 'v333')]
    # print(config.sections() )


# print(ini_遍历("demo.ini"))

def ini_删除():
    pass
    # 删    很少用到
    # 删除option  cf.remove_option('db', 'switch')  # 删除switch一项
    # 删除section cf.remove_section('db')  # 删除名为db的section下所有配置
