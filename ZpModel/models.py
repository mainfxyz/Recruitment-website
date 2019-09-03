from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Com(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)#一个user有一个公司

    name = models.CharField(max_length=10)
    tel = models.CharField(max_length=14)
    email = models.CharField(max_length=40)
    info = models.CharField(max_length=1000)
    type = models.CharField(max_length=4)
    ps = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '企业表'  # 首页列表的显示名称
        verbose_name="企业数据"  # 列表页和详情页的显示名称


class Zp(models.Model):
    url = models.CharField(max_length=100,null=True)
    company = models.CharField(max_length=30)
    jobType = models.CharField(max_length=40)
    jobName = models.CharField(max_length=40)
    W1 = models.IntegerField()#workingExp W1~W2
    W2 = models.IntegerField()
    eduLevel = models.CharField(max_length=10)
    K1 = models.FloatField()#salary K1~K2
    K2 = models.FloatField()
    info =models.CharField(max_length=200,default="",null=True)
    addr = models.CharField(max_length=60,default="",null=True)

    com_id = models.IntegerField(null=True)#com有多个zp

    def __str__(self):
        return self.jobName

    class Meta:
        verbose_name_plural = '招聘表'  # 首页列表的显示名称
        verbose_name="招聘数据"  # 列表页和详情页的显示名称

class CV(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)#一个user有一个简历

    sex = models.CharField(max_length=2,default="",null=True)
    age = models.IntegerField(null=True)
    edu = models.CharField(max_length=4,default="",null=True)
    super = models.CharField(max_length=10,default="",null=True)
    tech = models.CharField(max_length=10,default="",null=True)
    tel = models.CharField(max_length=14,default="",null=True)
    K1 = models.IntegerField(null=True)
    K2 = models.IntegerField(null=True)
    exp = models.IntegerField(null=True)
    wantJob = models.CharField(max_length=20,default="",null=True)
    school = models.CharField(max_length=20,default="",null=True)
    gzjl = models.CharField(max_length=200,default="",null=True)
    jybj = models.CharField(max_length=200,default="",null=True)
    zwjs = models.CharField(max_length=200,default="",null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = '简历表'  # 首页列表的显示名称
        verbose_name="简历数据"  # 列表页和详情页的显示名称

class CV2Zp(models.Model):
    user_id = models.IntegerField()
    zp_id = models.IntegerField()
    com_id=models.CharField(max_length=10,null=True)
    jobName = models.CharField(max_length=40,null=True)
    name = models.CharField(max_length=40,null=True)
    email = models.CharField(max_length=40,null=True)

    def __str__(self):
        return str(self.user_id)+" to "+str(self.zp_id)

    class Meta:
        verbose_name_plural = '投递关系表'  # 首页列表的显示名称
        verbose_name="投递关系数据"  # 列表页和详情页的显示名称
        unique_together = ("user_id", "zp_id")