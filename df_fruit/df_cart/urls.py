# coding=utf-8
from django.conf.urls import url

from df_cart import views

urlpatterns = [
    url(r'^add/$',views.cart_add),  # 添加购物车
    url(r'^count/$', views.car_count),  # 统计购物车数量
    url(r'^$', views.cart_list),  # 显示购物车
    url(r'^update/$', views.car_count_update),  # 显示购物车

]