import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from app01 import models

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        # fields = [""]
        exclude = ["oid","admin"] #单独排除一个 或者多个



def order_list(request):
    ''' 订单列表 '''
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    content = {
        "form":form,
        "queryset":page_object.page_queryset,
        "page_string":page_object.html(),
        "error":page_object.error,


    }

    return render(request,"order_list.html" ,content)


@csrf_exempt
def order_add(request):
    ''' 添加订单 '''
    form =  OrderModelForm(data = request.POST)
    if form.is_valid():

        # 获取 当前时间+随机数（1000~9999） ->（生成）  订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        
        return JsonResponse({"status":True})
        # return HttpResponse(json.dumps({"status":True}))

    return JsonResponse({"status":False,"error":form.errors})



def order_delete(request):
    ''' 删除订单 '''
    uid = request.GET.get("uid")
    exists = models.Order.objects.filter(id = uid).exists()
    
    if not exists:
        return JsonResponse({"status":False,"error":"删除失败，数据不存在！"})
    models.Order.objects.filter(id = uid).delete()
    return JsonResponse({"status":True})


def order_detail(request):
    ''' 根据ID获取订单详细信息 '''
    uid = request.GET.get("uid")
    
    #返回数据库中的一个对象  Order object (16)
    # row_object = models.Order.objects.filter(id = uid).first()

    row_dict = models.Order.objects.filter(id = uid).values("title","price","status").first()
    if not row_dict:
        return JsonResponse({"status":False,"error":"数据不存在！"})

    data = {
        "status":True,
        "data":row_dict,
    }
    return JsonResponse(data)


@csrf_exempt
def order_edit(request):
    ''' 订单编辑保存 '''
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id = uid).first()
    if not row_object:
        return JsonResponse({"status":False,"tips":"数据不存在！"})
    

    #表单验证
    form = OrderModelForm(data=request.POST,instance = row_object)
    # print("form :",form)

    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    

    return JsonResponse({"status":False,"error":form.errors})
