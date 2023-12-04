
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from app01.utils.bootstrap import BootStrapModelForm

# """"    ModelForm用法   """"
class UserModelForm(BootStrapModelForm):

    name = forms.CharField(min_length=2 , label="姓名")
    password = forms.CharField(min_length=3 , label="密码")

    class Meta:
        model = models.UserInfo
        fields = ["name","gender","password","position"
                  ,"age","account","create_time"
                  ,"depart"]


class PrettyNumModelForm(BootStrapModelForm):
    #验证方法1：
    number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误")]
    )

    class  Meta:
        model = models.PrettyNum
        fields = ["number","price","level","status"]
