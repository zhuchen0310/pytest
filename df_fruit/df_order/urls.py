# coding=utf-8
from django.conf.urls import url

from df_order import views

urlpatterns =[
    url(r'^$',views.order_show), # 显示订单页面视图

]