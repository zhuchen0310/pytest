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
    return JsonResponse({'res':car_count})

# 显示购物车详情
@login_requied
def cart_list(request):
    possprot_id = request.session.get('possport_id')
    #1.获取用户购物车的所有信息
    cart_list = Cart.objects_logic.get_car_list_by_possport_id(possport_id=possprot_id)
    return render(request,'cart.html',{'cart_list':cart_list})

# 更新用户购物车数据库信息
@require_GET
@login_requied
def car_count_update(request):
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passprot_id = request.session.get('possport_id')
    res = Cart.objects.update_cart_goods_info(goods_id=goods_id,goods_count=int(goods_count),possport_id=passprot_id)
    if res:
        return JsonResponse({'res':1})
    return JsonResponse({'res':0})

def delete_cart_info(request):
    cart_id = request.GET.get('cart_id')
    delete_info = Cart.objects.delete_cart_by_id(cart_id=cart_id)
    if delete_info:
        return JsonResponse({'res':1})
    else:
        return JsonResponse({'res':0})
