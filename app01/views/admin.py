from typing import Any, Dict
from django.shortcuts import render,redirect
from django import forms
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5




def admin_list(request):
    '''管理员列表'''

    # info_dict = request.session["info"]
    # print(info_dict["id"])
    # print(info_dict["name"])

    data_dict = {} #创建一个字典
    search_data = request.GET.get('q','') #获取get请求 查看q是否传值 有的话赋值
    if search_data: #判断是否获取到值
        data_dict["username__contains"] = search_data # 这里是存入数组 
        #在数据库中“username__contains”是选出包含search_data字段的所有数据
    
    queryset = models.Admin.objects.filter(**data_dict) #在数据库中找出所匹配的数据
    page_object = Pagination(request,queryset) #Pagination 一个自己写的分页 进行引入

    context = {
        "search_data":search_data,
        "queryset":page_object.page_queryset,
        "page_string" : page_object.html(),
        "error" : page_object.error,
    }

    return render(request,"admin_list.html",context)



class  AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value= True) #(render_value= True) 保留之前所写的 密码不会消失
    )

    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
            "password":forms.PasswordInput(render_value=True) #(render_value= True) 保留之前所写的 密码不会消失
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")

        return md5(pwd)

    def clean_confirm_password(self):
        
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd :
            raise ValidationError("确认密码输入不一致")
        
        # return返回什么 数据库就存储什么
        return confirm
         

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


def admin_add(request):
    '''管理员添加'''

    title = "添加管理员"

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request , "public_add.html",{"title":title,"form":form})
    
    form = AdminModelForm(data = request.POST)

    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/admin/list/")

    return render(request , "public_add.html" ,{"title":title,"form":form})



def admin_edit(request,nid):
    ''' 管理员编辑 '''
    title  = '编辑管理员页面'
    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object: #判断数据是否存在
        return redirect("/admin/list")
        # return render(request,"error.html")

    if request.method == "GET":
        form = AdminEditModelForm(instance = row_object)
        # form = AdminEditModelForm() # instance = row_object加上就能显示之前数据 

        return render(request,"public_add.html" ,{"title":title,"form":form})

    form = AdminEditModelForm(data = request.POST,instance = row_object)
    if form.is_valid():

        form.save()
        return redirect("/admin/list/")
    
    return render(request,"public_add.html" ,{"title":title,"form":form})



def admin_delete(request,nid):
    ''' 删除管理员 '''

    models.Admin.objects.filter(id = nid).delete()
    return redirect("/admin/list/")



class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value= True) #(render_value= True) 保留之前所写的 密码不会消失
    )

    class Meta:
        model = models.Admin
        fields = ['password','confirm_password']
        widgets = {
            "password":forms.PasswordInput(render_value=True) #(render_value= True) 保留之前所写的 密码不会消失
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        
        #去数据库进行对比（功能不能让其输入的密码跟原密码一样）
        exists = models.Admin.objects.filter(id = self.instance.pk,password = md5_pwd).exists()
        if exists:
            raise ValidationError("新密码与原密码一致")
        return md5_pwd

    def clean_confirm_password(self):
        
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd :
            raise ValidationError("确认密码输入不一致")
        
        # return返回什么 数据库就存储什么
        return confirm

def admin_reset(request,nid):
    ''' 管理员密码重置 '''
    title = '管理员密码重置'
    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object:
        return redirect("/admin/list/")

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request , "public_add.html",{"title":title,"form":form})
    
    form = AdminResetModelForm(request.POST,instance = row_object)

    if form.is_valid():
        form.save()

        return redirect("/admin/list/")
    
    return render(request , "public_add.html",{"title":title,"form":form})

