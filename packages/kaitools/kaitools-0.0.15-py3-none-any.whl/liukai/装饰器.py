# timefunc装饰器
def timefunc(func):
    # 作为装饰器使用，返回函数执行需要花费的时间
    # 任意函数  只要def funcname(...)的上方加了@timefunc 就可以被装饰

    import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, "函数,总计耗时:", time.time() - t, "秒")
        return result

    return wrapper


# try装饰器
def tryfunc(func):
    # 作为装饰器使用，返回函数执行需要花费的时间
    # 任意函数  只要def funcname(...)的上方加了@timefunc 就可以被装饰

    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # print(func.__name__, "函数,总计耗时:", time.time() - t, "秒")
            return result
        except:
            print("except")

    return wrapper
