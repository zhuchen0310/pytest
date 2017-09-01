# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^register/$', views.register),  # 注册页面

    url(r'^login/$', views.login),  # 登录页面
    url(r'^check_user_name_exist/$', views.check_user_name_exist),  # 用户名占用验证
    url(r'^login_check/$', views.login_check),  # 登录验证
    url(r'^$', views.user),  # 显示用户中心
    url(r'^order/$', views.user_order),  # 显示用户订单
    url(r'^address/$', views.user_addr),  # 显示用户收货地址
    url(r'^logout/$', views.logout),  # 退出登录

]
