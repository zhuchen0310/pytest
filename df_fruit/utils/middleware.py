# coding=utf-8


# 记录最近一次访问的url中间件
class UrlRecordMiddleWare(object):
    '''记录最后一次访问的有效url'''
    exclud_path = ['/user/login/', '/user/register/', '/user/check_user_name_exist/', '/user/login_check/',
                   '/user/logout/']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in UrlRecordMiddleWare.exclud_path:
            request.session['pre_url_path'] = request.get_full_path()
