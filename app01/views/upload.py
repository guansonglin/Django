
'''
文件上传 保存的实例 应用
'''

import os

from django import forms
from django.conf import settings

from app01 import models
from django.shortcuts import render,HttpResponse
from app01.utils.bootstrap import BootStrapForm,BootStrapModelForm

def upload_list(request):
    ''' 文件的提交 '''
    if request.method == 'GET':
        return  render(request,'upload_list.html')

    # print(request.POST)  #<QueryDict: {'csrfmiddlewaretoken': ['v4s55Zw0lXzqBATIUeDsfc1M2Yg9WKlnf14j4pvqSuJTjNylgbR1iMkioC3uurub'], 'username': ['test']}>
    # print(request.FILES)  #<MultiValueDict: {'avatar': [<TemporaryUploadedFile: 1684314364022.jpg (image/jpeg)>]}>

    file_object = request.FILES.get('avatar') #取出上传的文件名字
    # print(file_object)  # 1684314364022.jpg

    f = open(file_object,mode='wb') # file_object 可以自己命名，也可以上传文件本名称
    #文件读取
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return  HttpResponse("上传成功！")


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    ''' 混合文件上传（form） '''
    title = '文件上传'
    if request.method == 'GET':
        form = UpForm()
        return render(request , 'upload_form.html',{"form":form,"title":title})

    form = UpForm(data = request.POST , files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data.get('img'))
        image_object = form.cleaned_data.get('img')

        # db_file_path = os.path.join("static","img",image_object.name)

        # media_path = os.path.join(settings.MEDIA_ROOT,image_object.name)
        media_path = os.path.join('media',image_object.name)

        # file_path = os.path.join('app01',db_file_path)
        f = open(media_path,mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        

        models.Boss.objects.create(
            name = form.cleaned_data['name'],
            age = form.cleaned_data['age'],
            img = media_path,
        )
        return HttpResponse("...")

    return render(request , 'upload_form.html',{"form":form,"title":title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"

def upload_model_form(request):
    ''' 混合文件上传（modelform） '''
    title = 'modelfrom上传'
    if request.method == "GET":
        form = UpModelForm()

        return render(request,'upload_model_form.html',{"form":form,"title":title})
    
    form = UpModelForm(data = request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("上传成功")
    return render(request,'upload_model_form.html',{"form":form,"title":title})


