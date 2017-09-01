# coding=utf-8
from django.db import models
import copy


# 模型管理基类
class BaseManager(models.Manager):

    # 获取self所在模型类有效属性的字符串列表
    def get_all_valid_fields(self):
        # 1.获取self所在的模型类
        model_class = self.model
        # 2.获取model_class类型属性的元组
        attr_tuple = model_class._meta.get_fields()
        # 3.定义一个列表用来存储所有属性
        str_attr_list = []
        # 4.遍历元组
        for attr in attr_tuple:
            # 4.1 是否有关联外键
            if isinstance(attr, models.ForeignKey):
                # 4.2 外键字段名称为 属性名称_id
                str_attr = '%s_id' % attr.name
                print str_attr
            else:
                # 4.3 取出其他属性名称
                str_attr = attr.name
            # 4.4 添加到列表里
            str_attr_list.append(str_attr)
        # 5.返回包含所有属性的列表[goods_id,,]
        return str_attr_list

    # 添加一个self所在模型类的对象
    def create_one_object(self, **kwargs):
        # 1.获取self所在模型类有效属性字符串列表
        valid_fields = self.get_all_valid_fields()
        # 2.copy一份用于遍历
        kws = copy.copy(kwargs)
        # 3.去除kwargs中的无用参数
        for key in kws:
            if key not in valid_fields:
                kwargs.pop(key)
        # 4.获取self所在模型类的对象
        model_class = self.model
        # 5.创建一个model_class的对象
        obj = model_class(**kwargs)
        # 6.保存
        obj.save()
        # 7.返回这个对象
        return obj

    # 根据条件查询slef模型的对象
    def get_one_object(self, **filters):
        try:
            obj = self.get(**filters)
            # 报异常返回None
        except self.model.DoesNotExist:
            obj = None
        return obj

    # 根据条件查询self模型的查询集
    def get_object_list(self, filters={}, exclud_filters={}, order_by=('-pk',)):
        object_list = self.filter(**filters).exclude(**exclud_filters).order_by(*order_by)

        return object_list
