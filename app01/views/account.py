
from django.shortcuts import render,redirect,HttpResponse
from django import forms
from io import BytesIO

from app01 import models
from app01.utils.bootstrap import BootStrapForm,BootStrapModelForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code

class LoginFrom(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True #必须填写 不能为空
    )
    password = forms.CharField(
        label="密码",
        #widget=forms.PasswordInput, 
        widget=forms.PasswordInput(render_value=True), #render_value=True让这个字段在前端保留用户输入的数据
        required=True #必须填写 不能为空
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True #必须填写 不能为空
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    ''' 账号登录 '''
    if request.method == "GET":
        form = LoginFrom()  
        return render(request,"login.html",{"form":form})

    form = LoginFrom(data = request.POST)
    if form.is_valid():
        # print('cleaned_data',form.cleaned_data)


        #验证码的校验
        user_code_input = form.cleaned_data.pop('code')  #pop()当取出后在进行删除 我们数据库没有存储code字段 下面的数据库就查找不到
        code = request.session.get('image_code',"")
        if code.upper() != user_code_input.upper():
            form.add_error("code","验证码错误")
            return render(request,"login.html",{"form":form})


        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        print('admin_object',admin_object)
        if not admin_object:
            form.add_error("password","用户名或者密码错误")
            return render(request,"login.html",{"form":form})
            
        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = { 'id':admin_object.id,'name':admin_object.username }
        #session 只能保存1天
        request.session.set_expiry(60 * 60 * 24 * 1)
        return redirect("/admin/list/")
    
    return render(request,"login.html",{"form":form})
    


def image_code(reuqest):
    ''' 验证码的生成 '''

    # 调用pillow函数，生成图片
    img,code_string = check_code()

    reuqest.session['image_code'] = code_string
    #验证码只有60秒有效
    reuqest.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream , 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    ''' 账号退出 '''
    request.session.clear()
    return redirect('/login/')

