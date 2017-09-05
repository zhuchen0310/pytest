# coding=utf-8
from django.db import models
from django.db.models import Sum
from df_goods.models import GoodsImages, Goods
from db.Base_models import BaseModel
from db.Base_manager import BaseManager
from df_goods.models import GoodsImages

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

    # 根据cart_id_list 查询商品信息
    def get_cart_list_by_id_list(self,cart_id_list):
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart in cart_list:
            images = GoodsImages.objects.get_image_by_goods_id(goods_id=cart.goods.id)
            cart.goods.img_url = images.img_url
        return cart_list


class CartManager(BaseManager):
    '''购物车管理类'''

    # 根据用户id和商品id 查购物车信息
    def get_possport_cart_info(self, possport_id, goods_id):
        car_info = self.get_one_object(possport_id=possport_id, goods_id=goods_id)
        return car_info

    # 添加一个购物车信息
    def add_car_goods_info(self, possport_id, goods_id, goods_count):
        car_info = self.get_possport_cart_info(possport_id=possport_id, goods_id=goods_id)
        if car_info:
            car_info.goods_count = int(car_info.goods_count) + int(goods_count)
            car_info.save()
        else:

            car_info = self.create_one_object(possport_id=possport_id, goods_id=goods_id, goods_count=goods_count)

        return car_info

    # 根据用户id查商品数量
    def get_cart_count_by_passprot(self, possport_id):
        res_dict = self.get_object_list(filters={'possport_id': possport_id}).aggregate(Sum('goods_count'))
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res

    # 根据用户id查购物车信息
    def get_car_list_by_possport_id(self, possport_id):
        car_list = self.get_object_list(filters={'possport_id': possport_id})

    # 根据用户id 更新数据库信息
    def update_cart_goods_info(self, possport_id, goods_id, goods_count):
        cart_info = Cart.objects.get_possport_cart_info(possport_id=possport_id, goods_id=goods_id)
        if cart_info.goods.goods_stock < goods_count:
            return False  # 库存不足
        else:
            cart_info.goods_count = goods_count
            cart_info.save()
            return True

    # 根据购物车id删除购物车信息
    def delete_cart_by_id(self, cart_id):
        try:
            cart_info = self.get_one_object(id=cart_id)
            cart_info.delete()
            return True
        except Exception as e:
            return False

    # 根据cart_id_List 查 商品信息
    def get_cart_list_by_id_list(self,cart_id_list):
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        return cart_list

    # 根据cart_id_list 查 商品总数 和总价
    def get_goods_count_and_total_sprice_by_id_list(self,cart_id_list):
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        total_count,total_price = 0,0
        for cart in cart_list:
            total_count += cart.goods_count
            total_price += cart.goods.goods_price*cart.goods_count
        return total_count,total_price
class Cart(BaseModel):
    # 购物车模型
    possport = models.ForeignKey('df_user.Possport', verbose_name='所属用户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数量')

    objects = CartManager()
    objects_logic = CarLogicManager()

    class Meta:
        db_table = 's_cart_goods'
