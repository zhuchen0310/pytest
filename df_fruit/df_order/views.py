# coding=utf-8
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from df_cart.models import Cart
from utils.decorators import login_requied
from django.views.decorators.http import require_GET, require_POST
from df_user.models import Address
from df_order.models import OrderBasic,OrderDetail
# Create your views here.


@require_POST
@login_requied
# 订单页面
def order_show(request):
    # 获取登录用户信息
    passprot_id = request.session.get('possport_id')
    # 查询用户地址信息
    addr = Address.objects.get_default_addr(possport_id=passprot_id)
    # 获取传来的Cart_List_id
    cart_id_list = request.POST.getlist('cart_id_list')
    # 根据cart_id_list 查询用户商品信息
    cart_info_list = Cart.objects_logic.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    # cart_id_list 转换成字符串
    cart_id_list = ','.join(cart_id_list)
    context = {
        'addr':addr,
        'cart_id_list':cart_id_list,
        'cart_list':cart_info_list
    }
    return  render(request,'order.html',context)

# # 提交订单
# # 创建事务
# # @transaction.atomic
# @require_POST
# @login_requied
# def order_commit(request):
#     addr_id = request.POST.getlist('addr_id')
#     cart_id_list = request.POST.get('cart_id_list')
#     passprot_id = request.session.get('possport_id')
#     order_id = time.strftime("%Y%m%d%H%M%S",time.localtime())+str(passprot_id)
#     pay_method = request.POST.get('pay_method')
#     transit_price = 10
#     cart_id_list = cart_id_list.split(',')
#     total_sprice,total_count = Cart.objects.get_goods_count_and_total_sprice_by_id_list(cart_id_list=cart_id_list)
#     # 创建一个事务的记录点
#     # save_id = transaction.savepoint()
#     # try:
#     #     # 创建订单基本信息
#     OrderBasic.objects.add_one_order_basic_info(order_id=order_id,passprot_id=passprot_id,addr_id=addr_id,
#                                                     pay_method=pay_method,total_sprice=total_sprice,
#                                                     total_count=total_count,transit_price=transit_price)
#     #     # 创建订单详情信息
#     #
#     #     # 订单号  包含商品 商品数量 商品价格
#     #     # 根据购物车id列表查购物车信息
#     cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
#     for cart_info in cart_list:
#     #         # 创建一个订单详情cart
#             goods_count = cart_info.goods_count
#             goods_id = cart_info.goods.id
#             goods_price = cart_info.goods.goods_price
#     #         # 商品足够 创建
#             if goods_count < cart_info.goods.goods_stock:
#                 OrderDetail.objects.add_one_order_detail_info(order_id=order_id,goods_id=goods_id,goods_count=goods_count,
#                                                                      goods_price=goods_price)
#     #             # 清空掉购物车
#                 cart_info.delete()
#     #             # 修改商品库存和销量
#                 cart_info.goods.goods_stock -= goods_count
#                 cart_info.goods.goods_sales += goods_count
#     #
#     #         # 库存不足
#             else:
#                 # transaction.savepoint_rollback(save_id)
#                 return JsonResponse({'res':0,'content':'库存不足'})
#     #
#     # except Exception as e:
#     #     # 回滚到事务保存点
#     #     transaction.savepoint_rollback(save_id)
#     #     print e
#     #     return  JsonResponse({'res':-1,'content':'数据库异常'})
#
#     # 提交成功
#     # transaction.savepoint_commit(save_id)
#     return JsonResponse({'res':1})




# 事务
@require_POST
@login_requied
@transaction.atomic
def order_commit(request):
    '''
    创建订单信息
    '''
    # 1.接收信息
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')#1,2,3
    # 2.获取passport_id
    passprot_id = request.session.get('possport_id') # 数字
    # 3.组织订单信息 20170903153611+passport_id
    order_id = time.strftime("%Y%m%d%H%M%S",time.localtime())+str(passprot_id)
    transit_price = 10.0
    # print(order_id)
    # count,total_price get_goods_count_and_amout_by_id_list(cart_id_list)
    cart_id_list = cart_id_list.split(',')
    total_count,total_price = Cart.objects.get_goods_count_and_total_sprice_by_id_list(cart_id_list=cart_id_list)

    # 创建一个保存点
    save_id = transaction.savepoint()
    try:
        # 创建订单基本信息
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id, passprot_id=passprot_id,
                                                    addr_id=addr_id, total_count=total_count,
                                                    total_price=total_price, transit_price=transit_price,
                                                    pay_method=pay_method)

        # 遍历创建订单详情信息
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 组织订单详情数据
            goods_id = cart_info.goods.id
            goods_count = cart_info.goods_count
            goods_price = cart_info.goods.goods_price

            # 判断商品库存是否足够
            if goods_count < cart_info.goods.goods_stock:
                # 库存充足

                OrderDetail.objects.add_one_order_detail_info(order_id=order_id, goods_id=goods_id,
                                                              goods_count=goods_count, goods_price=goods_price)

                # 清空购物车
                cart_info.delete()

                # 修改商品的库存和销量
                cart_info.goods.goods_stock = cart_info.goods.goods_stock - goods_count
                cart_info.goods.goods_sales = cart_info.goods.goods_sales + goods_count
                cart_info.goods.save()
            else:
                # 库存不足
                # transaction.savepoint_rollback(save_id)
                return JsonResponse({'res':0, 'content':'库存不足'})
    except Exception as e:
        # 出现异常
        # transaction.savepoint_rollback(save_id)
        print e
        return JsonResponse({'res':-1, 'content':'服务器错误'})

    # transaction.savepoint_commit(save_id)
    return JsonResponse({'res':1})