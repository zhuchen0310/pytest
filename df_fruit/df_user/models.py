# coding=utf-8
from django.db import models
from db.Base_models import BaseModel
from db.Base_manager import BaseManager


# Create your models here.


# 用户信息管理模型类
class PossportManager(BaseManager):
    # 1.添加一条用户信息
    def add_one_possport(self, username, password, email):
        possport = self.create_one_object(username=username, password=password, email=email)
        return possport

    # 2.根据用户名密码查用户信息
    def get_one_possport(self, username, password=None):
        if password is None:
            possport = self.get_one_object(username=username)
        else:
            possport = self.get_one_object(username=username, password=password)
        return possport


# 用户信息模型
class Possport(BaseModel):
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PossportManager()

    class Meta:
        db_table = 's_user_info'


# 收货地址管理类
class AddressManager(BaseManager):
    # 获得账户的默认地址
    def get_default_addr(self, possport_id):
        addr = self.get_one_object(possport_id=possport_id, is_def=True)
        return addr

    # 添加一个收货地址
    def add_one_addr(self, possport_id, recipient_name, recipient_addr, recipient_phone, zip_code):
        # 查询是否有默认地址
        def_addr = self.get_default_addr(possport_id=possport_id)
        if def_addr:
            addr = self.create_one_object(possport_id=possport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,
                                          recipient_phone=recipient_phone, zip_code=zip_code)
        else:
            addr = self.create_one_object(possport_id=possport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,
                                          recipient_phone=recipient_phone, zip_code=zip_code, is_def=True)
        return addr


# 用户收货地址模型
class Address(BaseModel):
    possport = models.ForeignKey('Possport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=20, verbose_name='收货姓名')
    recipient_addr = models.CharField(max_length=256, verbose_name='收货地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='收货电话')
    zip_code = models.CharField(max_length=6, verbose_name='收货邮编')
    is_def = models.BooleanField(default=False, verbose_name='默认地址')

    objects = AddressManager()  # 管理类对象

    class Meta:
        db_table = 's_user_address'
