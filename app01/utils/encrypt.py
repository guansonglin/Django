'''
md5的加密函数 直接进行调用 可以使用
其中使用了django的setting中自带的SECRET_KEY字段 进行加密


from xxx.xxx.xxx import md5

md5(需要加密的字段)
'''

import hashlib

from django.conf import settings

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))

    return obj.hexdigest()



'''
可以根据自己所定义的salt来进行加密
salt = 'XXXXX'
obj = hashlib.md5(salt.encode('utf-8'))
obj.update(data_string.encode('utf-8'))
return obj.hexdigest()
'''