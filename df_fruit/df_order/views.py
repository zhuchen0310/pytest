from django.shortcuts import render

# Create your views here.
def order_show(request):
    return  render(request,'order.html')