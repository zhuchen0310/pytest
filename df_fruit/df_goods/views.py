# coding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from enums import *
from models import Goods, GoodsImages
from django.http import JsonResponse
# 用来存取最近五个浏览的商品ID
URL_LIST = []


# 首页
def home_list_page(request):
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)
    seafoods_new = Goods.objects.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    seafoods = Goods.objects_logic.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=4)
    meats_new = Goods.objects.get_goods_list_by_type(goods_type_id=MEAT, limit=3, sort='new')
    meats = Goods.objects_logic.get_goods_list_by_type(goods_type_id=MEAT, limit=4)
    eggs_new = Goods.objects.get_goods_list_by_type(goods_type_id=EGGS, limit=3, sort='new')
    eggs = Goods.objects_logic.get_goods_list_by_type(goods_type_id=EGGS, limit=4)
    vegetables_new = Goods.objects.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')
    vegetables = Goods.objects_logic.get_goods_list_by_type(goods_type_id=VEGETABLES, limit=4)
    frozens_new = Goods.objects.get_goods_list_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    frozens = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FROZEN, limit=4)
    context = {'fruits_new': fruits_new, 'fruits': fruits, 'FRUIT': FRUIT,
               'seafoods_new': seafoods_new, 'seafoods': seafoods, 'SEAFOOD': SEAFOOD,
               'meats_new': meats_new, 'meats': meats, 'MEAT': MEAT,
               'eggs_new': eggs_new, 'eggs': eggs, 'EGGS': EGGS,
               'vegetables_new': vegetables_new, 'vegetables': vegetables, 'VEGETABLES': VEGETABLES,
               'frozens_new': frozens_new, 'frozens': frozens, 'FROZEN': FROZEN,
               }
    return render(request, 'index.html', context)


# 商品详情页
def goods_detail(request, goods_id):
    if goods_id not in URL_LIST[0:5]:
        URL_LIST.insert(0, goods_id)

    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    type_title = GOODS_TYPE[goods.goods_type_id]
    return render(request, 'detail.html', {'goods': goods, 'goods_new_li': goods_new_li,
                                           'type_title': type_title,
                                           })


# 商品种类详情页
def goods_list(request, goods_type_id, page_index):
    sort = request.GET.get('sort')
    type_title = GOODS_TYPE[int(goods_type_id)]
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, limit=2, sort='new')
    goods_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, sort=sort)
    # 分页
    page_index = int(page_index)  # 当前页
    page = Paginator(goods_li, 1)  # 每页2个
    pages = page.num_pages  # 页面总数
    if pages <= 5:  # 如果页面总数小于5
        page_li = range(1, pages + 1)
    elif page_index <= 3:  # 前三页
        page_li = range(1, 6)
    elif page_index >= pages - 2:  # 后三页
        page_li = range(pages - 4, pages + 1)
    else:  # 其他
        page_li = range(page_index - 2, page_index + 3)
    # page_li = page.page_range    # 返回页码列表[ ]
    goods_li = page.page(page_index)  # 第几页的数据
    return render(request, 'list.html',
                  {'goods_new_li': goods_new_li, 'goods_li': goods_li, 'sort': sort, 'type_id': goods_type_id,
                   'type_title': type_title, 'pages': page_li, 'goods_type_id': goods_type_id})

# 根据商品列表查询商品图片
def get_image_list(request):
    goods_id_list = request.GET.get('goods_id_list') #[1,2]
    goods_id_list = goods_id_list.split(',')
    image_list = GoodsImages.objects.get_image_list_by_goods_id_list(goods_id_list=goods_id_list)
    print image_list
    image_dic = {}
    for image in image_list:
        # 每次取出一张图片
        image_dic[image.goods_id] = image.img_url.name
    return JsonResponse({'image_dic':image_dic})


# 根据商品id列表查询图片列表
    # -----------------------------------###--------------------------------------
def get_image_by_id_list(request):
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    goods_dic = Goods.objects_logic.get_goods_list_by_id_list(goods_id_list=goods_id_list)
    return JsonResponse({'image_dic':goods_dic})





    # -----------------------------------###--------------------------------------


    # 根据商品列表查询商品图片
# def get_image_list(request):
#     goods_str = request.GET.get('goods_str')
#     goods_list = goods_str.split(',')
#     goods_list.pop()
#     print goods_list
#     image_list = GoodsImages.objects.get_object_list(filters={'goods_id__in':goods_list})
#     print image_list
#     image_dic = {}
#     for image in image_list:
#         image_dic[image.goods_id] = image.img_url.name
#
#     return JsonResponse({'image_dic':image_dic})