# coding=utf-8
from django.db import models
from tinymce.models import HTMLField

from db.Base_manager import BaseManager
from db.Base_models import BaseModel
from enums import *

# 商品模型管理类
class GoodsManager(BaseManager):
    # 根据商品id获取商品信息
    def get_goods_by_id(self,goods_id):
        goods = self.get_one_object(id=goods_id)
        return goods

    # 根据商品种类id 获取商品信息
    def get_goods_list_by_type(self,goods_type_id,limit=None,sort='default'):
        if sort=='new':
            order_by = ('-createtime',)
        elif sort == 'price':
            order_by = ('goods_price',)
        elif sort == 'hot':
            order_by = ('-goods_sales',)
        else:
            order_by = ('-pk',)
        goods_list = self.get_object_list(filters={'goods_type_id':goods_type_id},order_by=order_by)
        if limit:
            goods_list = goods_list[:limit]
        return goods_list


# 商品逻辑查询管理类
class GoodsLogicManger(BaseManager):
    # 通过商品种类id 查询商品信息
    def get_goods_list_by_type(self,goods_type_id,limit=None,sort = 'default'):
        goods_list = Goods.objects.get_goods_list_by_type(goods_type_id=goods_type_id,limit=limit,sort=sort)
        for goods in goods_list:
            # 根据商品的id查询商品的图片
            img = GoodsImages.objects.get_image_by_goods_id(goods_id=goods.id)
            goods.img_url = img.img_url
        return goods_list

    # 根据商品的id 获取商品的信息
    def get_goods_by_id(self,goods_id):
        # 根据商品id查询商品
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        # 根据商品id查询商品图片
        img = GoodsImages.objects.get_image_by_goods_id(goods_id=goods.id)
        # 给商品绑定一个图片的属性
        goods.img_url = img.img_url
        return goods
#-----------------------------------###--------------------------------------
    # 根据商品的id_list 查询商品信息
    def get_goods_list_by_id_list(self,goods_id_list):
        #循环便利列表 根据每个goods_id逻辑查询
        goods_dic = {}
        for goods_id in goods_id_list:
            goods = self.get_goods_by_id(goods_id)
            goods_dic[goods.id]=goods.img_url.name
        return goods_dic
# -----------------------------------###--------------------------------------


# 商品模型
class Goods(BaseModel):
    goods_type_choice = (
        (FRUIT,GOODS_TYPE[FRUIT]),
        (SEAFOOD,GOODS_TYPE[SEAFOOD]),
        (MEAT,GOODS_TYPE[MEAT]),
        (EGGS,GOODS_TYPE[EGGS]),
        (VEGETABLES,GOODS_TYPE[VEGETABLES]),
        (FROZEN,GOODS_TYPE[FROZEN])
)


    goods_type_id = models.SmallIntegerField(choices=goods_type_choice,verbose_name='商品种类')
    goods_name = models.CharField(max_length=20,verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=256, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品运费')
    goods_unite = models.CharField(max_length=20, verbose_name='商品单位')
    goods_info = HTMLField(verbose_name='商品详情')
    goods_stock = models.IntegerField(default=0, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    # 0.下线商品 1.上线商品
    goods_status = models.SmallIntegerField(default=1, verbose_name='商品状态')

    objects = GoodsManager()
    objects_logic = GoodsLogicManger()
    class Meta:
        db_table = 's_goods'

# 商品图片管理类
class ImageManger(BaseManager):
    #根据商品的id获取商品的图片
    def get_image_by_goods_id(self,goods_id):
        images = self.get_object_list(filters={'goods_id':goods_id}) # QuerySet None
        if images.exists():
            # 说明有图片
            images= images[0]
        else:
            images.img_url = '' # 没有图片就赋值一个空字符串
        return images

    #根据商品id_list查询商品图片
    def get_image_list_by_goods_id_list(self,goods_id_list):
        image_list = self.get_object_list(filters={'goods_id__in':goods_id_list})
        return image_list


# 商品图片模型
class GoodsImages(BaseModel):
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods', verbose_name='商品图片')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = ImageManger()

    class Meta:
        db_table = 's_goods_image'
