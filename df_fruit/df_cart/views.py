# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render

from df_goods.models import Goods
from utils.decorators import login_requied
from django.views.decorators.http import require_GET
from models import Cart


# Create your views here.
# 添加购物车

@require_GET
@login_requied
def cart_add(request):
    goods_count = request.GET.get('goods_count')
    goods_id = request.GET.get('goods_id')
    possprot_id = request.session.get('possport_id')
    # 查询用户当前数据库信息
    # 查库存
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods.goods_stock < int(goods_count):
        # 库存不足
        return JsonResponse({'res': 0})
    else:
        # 添加购物车信息
        Cart.objects.add_car_goods_info(possport_id=possprot_id, goods_id=goods_id, goods_count=goods_count)
        return JsonResponse({'res': 1})
#查询用户商品总数
@login_requied
def car_count(request):
    possprot_id = request.session.get('possport_id')
    car_count = Cart.objects.get_cart_count_by_passprot(possport_id=possprot_id)
    print car_count
    return JsonResponse({'res':car_count})