'''
session的用法
就是django的类方法
主要功能：在没有登录的情况下，是无法访问其他内容的
'''
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMindlleWare(MiddlewareMixin):
    def process_request(self,request):
        
        if request.path_info in  ['/login/','/image/code/']:
            return
        
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        

        return redirect('/login/')
