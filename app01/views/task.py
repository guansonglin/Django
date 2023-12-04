import json

from django import forms
from  django.shortcuts import HttpResponse,render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse

from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model =  models.Task
        fields = "__all__"
        widgets = {
            "detail":forms.TextInput,
            # "detail":forms.Textarea,
        }
        

def task_list(request):
    ''' 任务管理 '''
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = TaskModelForm()

    content = {
        "form":form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),       # 生成页码
        "error" :  page_object.error            #搜索框的错误
    }

    return render(request , "task_list.html",content)

#装饰器
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)

    data_dict = {"status":True , 'data':[11,22,33,44]} 
    return HttpResponse(json.dumps(data_dict))

@csrf_exempt
def task_add(request):
    ''' 任务添加 '''
    
    # print(request.POST)

    form = TaskModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status":True } 
        return HttpResponse(json.dumps(data_dict)) #  等同于 -> return JsonResponse({"status":True})
        

    data_dict = {"status":False,'error':form.errors } 
    return HttpResponse(json.dumps(data_dict , ensure_ascii=False))

