from django.shortcuts import render,redirect
from app01 import models
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.form  import UserModelForm,PrettyNumModelForm






def pretty_list(request):
    ''' 靓号列表 '''

    #靓号搜索
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict["number__contains"] = search_data


    queryset = models.PrettyNum.objects.filter(**data_dict)

    page_object = Pagination(request ,queryset)

    #切片操作 分割数据
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    
    context = {

        "search_data":search_data,
        "queryset":page_object.page_queryset,
        "page_string":page_object.html() , 
        "error":page_object.error
        }
    

    return render(request , "pretty_list.html" ,context)



def pretty_add(reuqest):
    ''' 用户添加 '''
    if reuqest.method == "GET":
        form = PrettyNumModelForm()
        return render(reuqest , "pretty_add.html" ,{"form": form})

    form = PrettyNumModelForm(data = reuqest.POST)
    if form.is_valid():
        
        form.save()
        return redirect("/pretty/list/")

    return render(reuqest , "pretty_add.html" ,{"form":form})


def pretty_edit(request,nid):
    ''' 靓号编辑 '''
    row_project = models.PrettyNum.objects.filter(id = nid).first()
    if request.method == "GET":
        form = PrettyNumModelForm(instance = row_project)

        return render(request , "pretty_edit.html",{"form":form})

    form = PrettyNumModelForm(data = request.POST , instance = row_project)
    if form.is_valid():
        form.save()

        return redirect("/pretty/list/")
    
    return render(request,"pretty_edit.html",{"form":form})


def pretty_delete(request,nid):
    ''' 用户删除 '''
    models.PrettyNum.objects.filter(id = nid).delete()
    return redirect("/pretty/list")
