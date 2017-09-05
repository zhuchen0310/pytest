# coding=utf-8
from django.conf.urls import url

from df_order import views

urlpatterns =[
    url(r'^$',views.order_show), # 显示订单页面视图
    url(r'^commit/$',views.order_commit), # 订单提交页面
]