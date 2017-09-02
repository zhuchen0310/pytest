# coding=utf-8
from django.db import models
from django.db.models import Sum

from db.Base_models import BaseModel
from db.Base_manager import BaseManager
# Create your models here.

class CartManager(BaseManager):
    '''购物车管理类'''
    # 根据用户id和商品id 查购物车信息
    def get_possport_cart_info(self,possport_id,goods_id):
        car_info = self.get_one_object(possport_id=possport_id,goods_id=goods_id)
        return car_info

    def add_car_goods_info(self,possport_id,goods_id,goods_count):
        car_info = self.get_possport_cart_info(possport_id=possport_id,goods_id=goods_id)
        if car_info:
            car_info.goods_count = int(car_info.goods_count)+int(goods_count)
            car_info.save()
        else:
            car_info = self.create_one_object(possport_id=possport_id,goods_id=goods_id,goods_count=goods_count)

        return car_info

    def get_cart_count_by_passprot(self,possport_id):
        res_dict = self.get_object_list(filters={'possport_id':possport_id}).aggregate(Sum('goods_count'))
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res
class Cart(BaseModel):
    # 购物车模型
    possport = models.ForeignKey('df_user.Possport',verbose_name='所属用户')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(default=1,verbose_name='商品数量')

    objects = CartManager()
    class Meta:
        db_table = 's_cart_goods'