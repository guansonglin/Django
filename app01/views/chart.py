"""
这里面的数据都可以去数据库拿去

1.首先创建一个数据库
2.跟自己的需求进行填写
3.将数据导入出来


"""

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse


def chart_list(request):
    ''' 图表展示 '''

    return render(request,"chart_list.html")


def chart_line(request):
    ''' 折线图数据 '''
    
    legend = ['农夫山泉',"怡宝"]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月','7月','8月','9月','10月','11月','12月']
    series_list = [
                {
                    "name": '农夫山泉',
                    "type": 'line',
                    "data": [150, 300, 80, 418, 135, 350, 260, 500, 450, 350, 120, 255],
                },
                {
                    "name": '怡宝',
                    "type": 'line',
                    "data": [15, 200, 280, 118, 335, 50, 160, 100, 250, 150, 320, 80]
                }
                ]
    
    data_list = {
        "status":True,
        "data":{
            'legend':legend,
            'x_axis':x_axis,
            'series_list':series_list,
        }
    }

    return JsonResponse(data_list)



def chart_bar(request):
    ''' 柱状图数据 '''
    
    legend = ['小花',"小明"]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']
    series_list = [
                {
                    "name": '小花',
                    "type": 'bar',
                    "data": [5, 20, 36, 10, 10, 20],
                },
                {
                    "name": '小明',
                    "type": 'bar',
                    "data": [15, 30, 5, 40, 60, 100]
                }
                ]
    
    data_list = {
        "status":True,
        "data":{
            'legend':legend,
            'x_axis':x_axis,
            'series_list':series_list,
        }
    }

    return JsonResponse(data_list)

def chart_pie(request):
    ''' 饼图数据 '''
    
    # legend = ['小花',"小明"]
    # x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']
    series_list = [
                    { 'value': 1048, 'name': '抖音' },
                    { 'value': 735, 'name': '微博' },
                    { 'value': 580, 'name': 'QQ' },
                    { 'value': 484, 'name': '小红书' },
                    { 'value': 300, 'name': '微信' }
                ]
    
    data_list = {
        "status":True,
        "data":{
            # 'legend':legend,
            # 'x_axis':x_axis,/
            'series_list':series_list,
        }
    }

    return JsonResponse(data_list)