# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from models import *
from utils.get_hash import get_hash
from utils.decorators import login_requied
from df_goods.views import URL_LIST
from df_goods.models import Goods
from df_order.models import OrderDetail,OrderBasic
# 注册页面
@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == "GET":
        # get请求直接显示
        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name')
        password = get_hash(request.POST.get('pwd'))
        email = request.POST.get('email')
        # 存入数据库
        possport = Possport.objects.add_one_possport(username=username, password=password, email=email)
        # 发送邮件
        return redirect('/user/login/')


# 用户名验证
def check_user_name_exist(request):
    username = request.GET.get('username')
    # 数据库查
    possport = Possport.objects.get_one_possport(username=username)
    if possport is None:
        return JsonResponse({'res': 1})  # 未注册
    else:
        return JsonResponse({'res': 0})  # 已注册


# 登录页面
def login(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES.get('username')
    else:
        username = ''
    return render(request, 'login.html', {'username': username})


# 登录验证
def login_check(request):
    username = request.POST.get('username')
    password = get_hash(request.POST.get('password'))
    '''TEST'''
    print password
    possport = Possport.objects.get_one_possport(username=username, password=password)
    print possport
    if possport is None:
        return JsonResponse({'res': 0})  # 用户密码错误
    else:
        # 中间件记录最后一次的url
        next = request.session.get('pre_url_path', '/')
        jres = JsonResponse({'res': 1, 'next': next})
        # 用户勾选了记住账户
        if request.POST.get('remember') == 'true':
            jres.set_cookie('username', username, 14 * 24 * 60 * 60)
        # 记住登录状态
        request.session['username'] = username
        request.session['possport_id'] = possport.id
        request.session['is_login'] = True
        return jres


# 退出账户
def logout(request):
    request.session.flush()
    return redirect('/')


# 显示用户中心页
@login_requied
def user(request):
    goods_list = []  # 存储最近浏览的五个商品
    list = URL_LIST[0:5]
    for goods_id in list:
        goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
        goods_list.append(goods)
    possport_id = request.session.get('possport_id')
    addr = Address.objects.get_default_addr(possport_id=possport_id)
    return render(request, 'user_center_info.html', {'page': 'user','addr':addr,'goods_list':goods_list})


# 显示用户订单页面
@login_requied
def user_order(request):
    passprot_id = request.session.get('possport_id')
    # 根据用户id查询所有订单信息
    order_basic_list = OrderBasic.objects_logic.get_order_basic_list_by_passprot(passprot_id=passprot_id)
    return render(request, 'user_center_order.html', {'page': 'order','order_basic_list':order_basic_list})


# 显示用户收货地址
@require_http_methods(['GET', 'POST'])
@login_requied
def user_addr(request):
    possport_id = request.session.get('possport_id')
    if request.method == 'POST':
        recipient_name = request.POST.get('uname')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        # 存入数据库
        Address.objects.add_one_addr(possport_id=possport_id, recipient_name=recipient_name,
                                     recipient_addr=recipient_addr,
                                     recipient_phone=recipient_phone, zip_code=zip_code)
        addr = Address.objects.get_default_addr(possport_id=possport_id)
    else:
        addr = Address.objects.get_default_addr(possport_id=possport_id)
    return render(request, 'user_center_site.html', {'page': 'addr', 'addr': addr})
