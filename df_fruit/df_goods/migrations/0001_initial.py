# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('goods_type_id', models.SmallIntegerField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe7\xa7\x8d\xe7\xb1\xbb', choices=[(1, b'\xe7\x94\x9f\xe9\xb2\x9c\xe6\xb0\xb4\xe6\x9e\x9c'), (2, b'\xe6\xb5\xb7\xe9\xb2\x9c\xe6\xb0\xb4\xe4\xba\xa7'), (3, b'\xe7\x8c\xaa\xe7\x89\x9b\xe7\xbe\x8a\xe8\x82\x89'), (4, b'\xe7\xa6\xbd\xe7\xb1\xbb\xe8\x9b\x8b\xe5\x93\x81'), (5, b'\xe6\x96\xb0\xe9\xb2\x9c\xe8\x94\xac\xe8\x8f\x9c'), (6, b'\xe9\x80\x9f\xe5\x86\xbb\xe9\xa3\x9f\xe5\x93\x81')])),
                ('goods_name', models.CharField(max_length=20, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('goods_sub_title', models.CharField(max_length=256, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x89\xaf\xe6\xa0\x87\xe9\xa2\x98')),
                ('goods_price', models.DecimalField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=10, decimal_places=2)),
                ('transit_price', models.DecimalField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe8\xbf\x90\xe8\xb4\xb9', max_digits=10, decimal_places=2)),
                ('goods_unite', models.CharField(max_length=20, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x8d\x95\xe4\xbd\x8d')),
                ('goods_info', tinymce.models.HTMLField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe8\xaf\xa6\xe6\x83\x85')),
                ('goods_stock', models.IntegerField(default=0, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\xba\x93\xe5\xad\x98')),
                ('goods_sales', models.IntegerField(default=0, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe9\x94\x80\xe9\x87\x8f')),
                ('goods_status', models.SmallIntegerField(default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe7\x8a\xb6\xe6\x80\x81')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('img_url', models.ImageField(upload_to=b'goods', verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87')),
                ('is_def', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xbb\x98\xe8\xae\xa4')),
                ('goods', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x95\x86\xe5\x93\x81', to='df_goods.Goods')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
