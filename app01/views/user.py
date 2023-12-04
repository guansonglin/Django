
from django.shortcuts import render,redirect
from app01 import models
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.form  import UserModelForm,PrettyNumModelForm



def user_list(request):
    ''' 用户列表 '''

    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request,queryset,page_data=2)

    context = {
        "queryset":page_object.page_queryset,
        "page_string":page_object.html(),
        "error" :page_object.error
        }


    return render(request , 'user_list.html',context )

def user_add(request):
    ''' 用户添加(原始方法) '''
    if request.method == "GET":
        context = {
            "gender_choices":models.UserInfo.gender_choices,
            "depart_list":models.Department.objects.all()

        }

        return render(request , "user_add.html",context)
    
    name = request.POST.get("name")
    gender = request.POST.get("gd")
    password = request.POST.get("pwd")
    position = request.POST.get("psn")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    create_time = request.POST.get("ct")
    depart_id = request.POST.get("dp")

    models.UserInfo.objects.create(name = name,password = password,position = position,
                                   age = age , account = account , create_time = create_time,
                                   gender = gender,depart_id = depart_id)
    
    return redirect("/user/list/")

def user_model_form_add(request):
    ''' 用户添加(ModelForm版本) '''
    if request.method == "GET":
        form = UserModelForm() 

        return render(request , "user_model_form_add.html",{"form": form})


    ''' 错误校验 和返回 '''
    form = UserModelForm(data = request.POST)
    if form.is_valid():

        form.save()
        return redirect("/user/list/")
    
    return render(request , "user_model_form_add.html",{"form": form})

def user_edit(request,nid):
    ''' 用户编辑 '''
    row_project = models.UserInfo.objects.filter(id = nid).first()
    if request.method == "GET":
        form = UserModelForm(instance = row_project)

        return render(request , 'user_edit.html',{"form":form})

    form = UserModelForm(data = request.POST , instance = row_project)
    if form.is_valid():

        form.save()
        return redirect("/user/list/")

    return render(request , 'user_edit.html',{"form":form})

def user_delete(request,nid):
    ''' 用户删除 '''
    models.UserInfo.objects.filter(id = nid).delete()
    return redirect("/user/list/")

