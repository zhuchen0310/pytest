# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('recipient_name', models.CharField(max_length=20, verbose_name=b'\xe6\x94\xb6\xe8\xb4\xa7\xe5\xa7\x93\xe5\x90\x8d')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name=b'\xe6\x94\xb6\xe8\xb4\xa7\xe5\x9c\xb0\xe5\x9d\x80')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name=b'\xe6\x94\xb6\xe8\xb4\xa7\xe7\x94\xb5\xe8\xaf\x9d')),
                ('zip_code', models.CharField(max_length=6, verbose_name=b'\xe6\x94\xb6\xe8\xb4\xa7\xe9\x82\xae\xe7\xbc\x96')),
                ('is_def', models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe5\x9c\xb0\xe5\x9d\x80')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
        migrations.CreateModel(
            name='Possport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('isDelete', models.BooleanField(default=False, verbose_name=b'\xe9\x80\xbb\xe8\xbe\x91\xe5\x88\xa0\xe9\x99\xa4')),
                ('username', models.CharField(max_length=20, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('password', models.CharField(max_length=40, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81')),
                ('email', models.EmailField(max_length=254, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1')),
            ],
            options={
                'db_table': 's_user_info',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='possport',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe8\xb4\xa6\xe6\x88\xb7', to='df_user.Possport'),
        ),
    ]
