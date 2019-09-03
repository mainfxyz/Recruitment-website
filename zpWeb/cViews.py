from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
import sys
sys.path.append("..")
from ZpModel.models import Zp,Com,CV2Zp,CV
from .view import loginfo,ZpListView
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.http import JsonResponse
import json

def cIndex(request):
    user = request.user

    #判断登录
    if not request.user.is_authenticated:
        return ZpListView.as_view()(request)
    u=User.objects.get(username=user)
    if u.last_name=="qy":
        try:
            com=Com.objects.get(user_id=u.id)
        except:#如果没有公司数据就创建一条
            c=Com(user_id=u.id)
            c.save()
        finally:
            return ComListView.as_view()(request)
    else:
        return ZpListView.as_view()(request)
        # 用户类型err!




class ComListView(ListView):
    name=""
    info=""
    ps=""
    tel=""
    email=""
    type=""

    user = "登录"
    model = Zp#数据源
    template_name = "cIndex.html"#网页链接
    paginate_by = 10  # if pagination is desired，分页每页的信息条数

#修改查询数据
    def get_queryset(self):
        u = User.objects.get(username=self.user)
        com = Com.objects.get(user_id=u.id)
        zps=Zp.objects.filter(com_id=com.id)
        return zps

    #添加返回数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user!=None and self.user!="" and not self.user.is_anonymous:
            context['user']='<i class="fa fa-user-circle" style="font-size:19px"></i>&nbsp'+str(self.user)+'</a>' \
                '&nbsp&nbsp&nbsp<a class="text-white" id="logout"> <i class="fa fa-sign-out" style="font-size:19px"></i>注销'
        else:
            context['user'] = '<i class="fa fa-sign-in" style="font-size:19px"></i>&nbsp&nbsp<span>登录</span>'

        u = User.objects.get(username=self.user)
        com = Com.objects.get(user_id=u.id)
        context['name'] = com.name
        context['info'] = com.info
        context['ps'] = com.ps
        context['type'] = com.type
        context['tel'] = com.tel
        context['email'] = com.email
        return context

#获取request
    def get(self, request, *args, **kwargs):
        self.name = request.GET.get('name')
        self.info = request.GET.get('info')
        self.ps = request.GET.get('ps')
        self.type = request.GET.get('type')
        self.tel = request.GET.get('tel')
        self.email = request.GET.get('email')
        self.user = request.user
        r=super().get(self, request, *args, **kwargs)
        return r








def save_com_info(request):
    user = request.user
    # 判断登录
    if not request.user.is_authenticated:
        return ZpListView.as_view()(request)

    name=request.GET.get('name','')
    type=request.GET.get('type','')
    ps=request.GET.get('ps','')
    tel=request.GET.get('tel','')
    email=request.GET.get('email','')
    info=request.GET.get('info','')

    u = User.objects.get(username=request.user)
    com = Com.objects.get(user_id=u.id)
    com.name=name
    com.type=type
    com.ps=ps
    com.tel=tel
    com.email=email
    com.info=info
    try:
        com.save()
    except:
        pass
    return HttpResponseRedirect('/cIndex')


def addZp(request):
    user = request.user
    # 判断登录
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    K1=request.GET.get('K1')
    K2=request.GET.get('K2')
    W1=request.GET.get('W1')
    W2=request.GET.get('W2')
    info=request.GET.get('zpInfo')
    eduLevel=request.GET.get('eduLevel')
    jobName=request.GET.get('jobName')
    jobType=request.GET.get('jobType')

    u = User.objects.get(username=user)
    com = Com.objects.get(user_id=u.id)
    zp = Zp()
    zp.com_id = com.id
    zp.company=com.name
    zp.W1=W1
    zp.W2=W2
    zp.K1=K1
    zp.K2=K2
    zp.info=info
    zp.eduLevel=eduLevel
    zp.jobName=jobName
    zp.jobType=jobType
    try:
        zp.save()
    except:
        pass
    #return HttpResponse(zp)
    return HttpResponseRedirect('/cIndex')

def saveZp(request):#缺少表连接验证权限
    user = request.user
    # 判断登录
    if not request.user.is_authenticated:
        return HttpResponseRedirect('cIndex')
    eduLevel=request.GET.get('eduLevel','')
    jobName=request.GET.get('jobName','')
    W1=request.GET.get('W1')
    W2 = request.GET.get('W2')
    K1=request.GET.get('K1')
    K2=request.GET.get('K2')
    p_id=request.GET.get('pid')

    zp=Zp.objects.get(id=p_id)
    zp.jobName=jobName
    zp.eduLevel=eduLevel
    zp.W1=W1
    zp.W2=W2
    zp.K1=K1
    zp.K2=K2
    try:
        zp.save()
    except:
        return HttpResponse('保存失败')
    return HttpResponse('保存成功')

def delZp(request):#缺少表连接验证权限
    user = request.user
    # 判断登录
    if not request.user.is_authenticated:
        return HttpResponseRedirect('cIndex')
    p_id = request.GET.get('pid')
    try:
        Zp.objects.get(id=p_id).delete()
    except:
        return HttpResponse('删除失败')
    return HttpResponse('删除成功')


class cAppli(ListView):
    user = ""
    model = CV2Zp#数据源
    template_name = "cAppli.html"#网页链接
    paginate_by = 10  # if pagination is desired，分页每页的信息条数

    def get_queryset(self):
        if self.user == None and self.user == "" and self.user.is_anonymous:
            raise Http404
        else:
            user_id=self.user.id
            com=Com.objects.get(user_id=user_id)
            com_id=com.id
            rs=CV2Zp.objects.filter(com_id=com_id)
            return rs

    # 添加返回数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user != None and self.user != "" and not self.user.is_anonymous:
            context['user'] = '<i class="fa fa-user-circle" style="font-size:19px"></i>&nbsp' + str(self.user) + '</a>' \
                                                                                                                 '&nbsp&nbsp&nbsp<a class="text-white" id="logout"> <i class="fa fa-sign-out" style="font-size:19px"></i>注销'
        else:
            context['user'] = '<i class="fa fa-sign-in" style="font-size:19px"></i>&nbsp&nbsp<span>登录</span>'
        return context

    # 获取request
    def get(self, request, *args, **kwargs):
        self.user = request.user
        r = super().get(self, request, *args, **kwargs)
        return r

def lookCV(request):
    user = request.user
    # 判断登录
    if not user.is_authenticated:
        return HttpResponse("请登录")
    user_id=request.GET.get('user_id')
    cv=CV.objects.filter(user_id=user_id).values()
    return HttpResponse(cv)


# def send(request):
#     from django.core.mail import send_mail
#     send_mail('应聘成功', '可以来面试，亲', '15610575692@163.com',
#               ['15610575692@163.com'], fail_silently=False)
#     return HttpResponse('OK')
#
# def refuse(request):
#     pass