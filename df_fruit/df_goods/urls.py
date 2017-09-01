# coding=utf-8
from django.conf.urls import url

from df_goods import views

urlpatterns = [
    url(r'^$', views.home_list_page),  # 首页
    url(r'^goods/(?P<goods_id>\d+)/$', views.goods_detail),  # 商品详情
    url(r'^lists/(?P<goods_type_id>\d+)/(?P<page_index>\d+)/$', views.goods_list),  # 商品种类详情
    url(r'^get_image_list/$',views.get_image_by_id_list) # 根据商品id列表查询商品图片
]
