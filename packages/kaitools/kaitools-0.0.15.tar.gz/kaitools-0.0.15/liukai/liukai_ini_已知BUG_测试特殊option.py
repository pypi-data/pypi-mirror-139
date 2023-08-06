from liukai.INI操作 import *

ini_write("url.ini", "kanxiaoshuo", "http://m.kanxiaoshuo.org/wapbook/35024.html", "yes")
ini_write("url.ini", "kanxiaoshuo", "http://m.kanxiaoshuo.org/wapbook/121212.html", "yes")
ini_write("url.ini", "kanxiaoshuo", "http://m.kanxiaoshuo.org/wapbook/22222.html", "yes")
ini_write("url.ini", "kanxiaoshuo", "http://m.kanxiaoshuo.org/wapbook/44444.html", "yes")

# configparser.DuplicateOptionError: While reading from 'url.ini' [line  3]: option 'http' in section 'kanxiaoshuo' already exists
# ■果然报bug了
