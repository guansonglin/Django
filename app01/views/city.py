
from django.shortcuts import render,redirect,HttpResponse

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


def city_list(request):
    ''' 城市展示 '''
    queryset = models.City.objects.all()
    return render(request,"city_list.html",{"queryset":queryset})


class UpModelFormCity(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = '__all__'
def city_add(request):
    ''' 城市添加 '''
    
    title = '城市添加'
    if request.method == 'GET':
        form = UpModelFormCity()
        return render(request,'city_add.html',{'form':form,'title':title})
    
    form = UpModelFormCity(data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')

    return render(request,'city_add.html',{'form':form,'title':title})