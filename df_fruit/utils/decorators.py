# coding=utf-8


# 用户登录验证装饰器
from django.shortcuts import redirect


def login_requied(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/user/login/')

    return wrapper
