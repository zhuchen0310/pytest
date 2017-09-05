# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBasic',
            fields=[
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('order_id', models.CharField(max_length=60, serialize=False, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe7\xbc\x96\xe5\x8f\xb7', primary_key=True)),
                ('total_price', models.DecimalField(verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe6\x80\xbb\xe4\xbb\xb7', max_digits=10, decimal_places=2)),
                ('total_count', models.IntegerField(default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f')),
                ('transit_price', models.DecimalField(verbose_name=b'\xe8\xbf\x90\xe8\xb4\xb9', max_digits=10, decimal_places=2)),
                ('pay_method', models.IntegerField(default=1, verbose_name=b'\xe6\x94\xaf\xe4\xbb\x98\xe6\x96\xb9\xe5\xbc\x8f')),
                ('order_status', models.IntegerField(default=1, verbose_name=b'\xe8\xae\xa2\xe5\x8d\x95\xe7\x8a\xb6\xe6\x80\x81')),
                ('addr', models.ForeignKey(verbose_name=b'\xe6\x94\xb6\xe8\xb4\xa7\xe5\x9c\xb0\xe5\x9d\x80', to='df_user.Address')),
                ('passprot', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\x94\xa8\xe6\x88\xb7', to='df_user.Possport')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('goods_count', models.IntegerField(default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe9\x87\x8f')),
                ('goods_price', models.DecimalField(verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=10, decimal_places=2)),
                ('goods', models.ForeignKey(verbose_name=b'\xe5\x8c\x85\xe5\x90\xab\xe5\x95\x86\xe5\x93\x81', to='df_goods.Goods')),
                ('order', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe8\xae\xa2\xe5\x8d\x95', to='df_order.OrderBasic')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
