from django.db import models

# Create your models here.


class Admin(models.Model):

    username = models.CharField(verbose_name="用户名" ,max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64) 

    def  __str__(self) -> str:
        return self.username


class Department(models.Model):
    ''' 部门表 '''
    title = models.CharField(verbose_name="部门",max_length=32)

    def __str__(self) -> str:
        return self.title



class UserInfo(models.Model):
    ''' 员工表 '''
    name = models.CharField(verbose_name= "姓名",max_length=16)
    password = models.CharField(verbose_name= "密码",max_length=64)
    position = models.CharField(verbose_name= "职位",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    # max_digits：数字允许的最大位数   decimal_places：小数的最大位数
    account = models.DecimalField(verbose_name="账户金额",max_digits=10,decimal_places=2 , default=0)
    # 在mysql里面有个datetime类型，在Django的ORM语言里面对应的类是DateTimieField。    
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")


    #超级连接删除
    depart = models.ForeignKey(to="Department",verbose_name= "部门" ,to_field="id",on_delete=models.CASCADE)

    # 在django中的约束
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )

    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)



class PrettyNum(models.Model):
    ''' 靓号表 '''
    
    number = models.CharField(verbose_name="手机号" , max_length=32)

    #默认情况可以为空 添加 ：null=True,blank=True
    price = models.IntegerField(verbose_name="价格",default=0) 

    level_choices = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别" , choices=level_choices , default=1)

    status_choices = (
        (1,"未购买"),
        (2,"已购买"),
    )

    status = models.SmallIntegerField(verbose_name="状态" ,choices=status_choices , default=1) #default 当他没有选的时候 默认选1


class Task(models.Model):
    '''任务表单'''
    level_choices = (
        (1,"紧急"),
        (2,"重要"),
        (3,"无关"),
    )

    level = models.SmallIntegerField(verbose_name="级别" ,choices=level_choices , default=1)

    title =  models.CharField(verbose_name="标题" , max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    user = models.ForeignKey(verbose_name="负责人" , to="Admin" , on_delete=models.CASCADE)


class Order(models.Model):
    ''' 订单表单 '''
    oid = models.CharField(verbose_name="订单号" , max_length=64)
    title = models.CharField(verbose_name="商品名称" , max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1,"待支付"),
        (2,"已支付"),
    )

    status = models.SmallIntegerField(verbose_name="状态" , choices=status_choices, default=1)

    admin = models.ForeignKey(verbose_name="管理员" , to="Admin" , on_delete=models.CASCADE)



class Boss(models.Model):
    ''' 老板（文件上传） '''
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像",max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")

    # 本质上数据库也是CharField，自动保存数据。
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')

