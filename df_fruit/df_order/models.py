# coding=utf-8
from django.db import models
from db.Base_manager import BaseManager
from db.Base_models import BaseModel
from df_goods.models import GoodsImages


# Create your models here.
# 基本信息逻辑管理类
class OrderBasicLogicManager(BaseManager):
    # 根据用户id查用户订单信息
    def get_order_basic_list_by_passprot(self, passprot_id):
        # 根据用户id 查订单基本信息 列表
        order_basic_list = OrderBasic.objects.get_order_info_list_by_passprot_id(passprot_id=passprot_id)
        # 遍历所有订单信息 加上订单详情信息
        for order_basic in order_basic_list:
            # 根据订单id 查询订单详情列表
            order_detail_list = OrderDetail.objects_logic.get_order_detail_list_by_order_id(order_basic.order_id)
            order_basic.order_detail_list = order_detail_list
        return order_basic_list


class OrderBasicManager(BaseManager):
    '''基本订单管理类'''

    # 创建一个基本订单
    def add_one_order_basic_info(self, order_id, passprot_id, addr_id, total_price, total_count, transit_price,
                                 pay_method):
        order_basic = self.create_one_object(order_id=order_id, passprot_id=passprot_id, total_price=total_price,total_count=total_count, transit_price=transit_price,pay_method=pay_method, addr_id=addr_id)
        return order_basic

    # 根据用户id查用户订单基本信息
    def get_order_info_list_by_passprot_id(self, passprot_id):
        order_basic_list = self.get_object_list(filters={'passprot_id': passprot_id})
        return order_basic_list


class OrderBasic(BaseModel):
    '''订单基本类'''
    order_id = models.CharField(max_length=60, primary_key=True, verbose_name='订单编号')
    passprot = models.ForeignKey('df_user.Possport', verbose_name='所属用户')
    addr = models.ForeignKey('df_user.Address', verbose_name='收货地址')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    pay_method = models.IntegerField(default=1, verbose_name='支付方式')
    order_status = models.IntegerField(default=1, verbose_name='订单状态')

    objects = OrderBasicManager()
    objects_logic = OrderBasicLogicManager()

    class Meta:
        db_table = 's_order_basic'


# 详情信息逻辑管理类
class OrderDetailLogicManager(BaseManager):
    # 根据订单 id 查询订单详情信息列表 带图片
    def get_order_detail_list_by_order_id(self, order_id):
        # 先不带图片
        order_detail_list = OrderDetail.objects.get_order_detail_list_by_order_id(order_id=order_id)
        # 遍历 给 订单详情加 图片
        for order_detail in order_detail_list:
            image = GoodsImages.objects.get_image_by_goods_id(goods_id=order_detail.goods.id)
            order_detail.img_url = image.img_url
        return order_detail_list

        # def get_order_detail_list_by_passport(self,passport_id):
        # 根据用户的id查询用户订单详情
        #     order_detail_list = self.get_object_list(filters={'passport_id':passport_id})
        #     return orderdetail_list


class OrderDetailManager(BaseManager):
    '''订单详情管理类'''

    # 创建订单详情信息
    def add_one_order_detail_info(self, order_id, goods_id, goods_count, goods_price):
        order_detail = self.create_one_object(order_id=order_id, goods_id=goods_id, goods_count=goods_count,
                                              goods_price=goods_price)
        return order_detail

    # 根据订单基本信息　查询用户订单详情信息
    # def get_order_derail_info_by_oreder_basic_info(self,order_basic_info):
    #     self.get_object_list(filters={'order'})

    # 根据订单id查询订单详情
    def get_order_detail_list_by_order_id(self, order_id):
        order_detail_list = self.get_object_list(filters={'order_id': order_id})
        return order_detail_list


class OrderDetail(BaseModel):
    '''定义订单详情类 '''
    order = models.ForeignKey('OrderBasic', verbose_name='所属订单')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='包含商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数量')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')

    objects = OrderDetailManager()
    objects_logic = OrderDetailLogicManager()

    class Meta:
        db_table = 's_order_detail'
