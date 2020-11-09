#!/usr/bin/python3

from inspect import signature


def check_type(*ty_args, **ty_kwargs):
    def out_wrapper(func):
        # 通过signature方法，获取函数形参：name, age, height
        sig = signature(func)
        # 获得装饰器传来的参数， 函数签名与之绑定，字典类型
        bind_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
        print(bind_types)

        def wrapper(*args, **kwargs):
            # 给执行函数中具体的实参进行和形参进行绑定，形成字典的形式
            func_type = sig.bind(*args, **kwargs).arguments.items()
            print(func_type)
            # 循环形参和实参字典的items()形式
            for name, obj in func_type:
                if name in bind_types:
                    if not isinstance(obj, bind_types[name]):
                        raise TypeError(
                            '%s must be %s' % (name, bind_types[name]))
            func(*args, **kwargs)

        return wrapper

    return out_wrapper


# 通过装饰器实现对函数参数进行类型检查
@check_type(str, int, float)
def func(name, age, height):
    print(name, age, height)


if __name__ == '__main__':
    func('bei_men', 18, 1.75)
