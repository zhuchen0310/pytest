# coding=utf-8
from django.db import models


# 模型基类
class BaseModel(models.Model):
    updatetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    createtime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    isDelete = models.BooleanField(verbose_name='逻辑删除', default=False)

    class Meta:
        abstract = True
