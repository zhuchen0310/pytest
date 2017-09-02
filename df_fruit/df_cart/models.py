# coding=utf-8
from django.db import models
from django.db.models import Sum
from df_goods.models import GoodsImages, Goods
from db.Base_models import BaseModel
from db.Base_manager import BaseManager
# Create your models here.
class CarLogicManager(BaseManager):
    '''购物车逻辑管理类'''

    # 根据用户id查购物车信息
    def get_car_list_by_possport_id(self, possport_id):
        car_list = self.get_object_list(filters={'possport_id': possport_id})
        for cart_info in car_list:
            img = GoodsImages.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return car_list
class CartManager(BaseManager):
    '''购物车管理类'''
    # 根据用户id和商品id 查购物车信息
    def get_possport_cart_info(self,possport_id,goods_id):
        car_info = self.get_one_object(possport_id=possport_id,goods_id=goods_id)
        return car_info
    #添加一个购物车信息
    def add_car_goods_info(self,possport_id,goods_id,goods_count):
        car_info = self.get_possport_cart_info(possport_id=possport_id,goods_id=goods_id)
        if car_info:
            car_info.goods_count = int(car_info.goods_count)+int(goods_count)
            car_info.save()
        else:
            car_info = self.create_one_object(possport_id=possport_id,goods_id=goods_id,goods_count=goods_count)

        return car_info
    # 根据用户id查商品数量
    def get_cart_count_by_passprot(self,possport_id):
        res_dict = self.get_object_list(filters={'possport_id':possport_id}).aggregate(Sum('goods_count'))
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res
    # 根据用户id查购物车信息
    def get_car_list_by_possport_id(self,possport_id):
        car_list = self.get_object_list(filters={'possport_id':possport_id})

    # 根据用户id 更新数据库信息
    def update_cart_goods_info(self,possport_id,goods_id,goods_count):
        cart_info = Cart.objects.get_possport_cart_info(possport_id=possport_id,goods_id=goods_id)
        if cart_info.goods.goods_stock < goods_count:
            return False # 库存不足
        else:
            cart_info.goods_count = goods_count
            cart_info.save()
            return True



class Cart(BaseModel):
    # 购物车模型
    possport = models.ForeignKey('df_user.Possport',verbose_name='所属用户')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(default=1,verbose_name='商品数量')

    objects = CartManager()
    objects_logic = CarLogicManager()
    class Meta:
        db_table = 's_cart_goods'