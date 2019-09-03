from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
import sys
sys.path.append("..")
from ZpModel.models import Zp,Com,CV

#原始的方法，函数编程，一步一步自己写
def logIN(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("用户不存在！")
    if check_password(password, user.password):
        login(request, user)
        return HttpResponse("登录成功")
    else:
        return HttpResponse("密码错误！")


def logOUT(request):
    logout(request)
    return HttpResponse(str(request.POST))

def reg(request):
    name = request.GET.get('name')
    username = request.GET.get('username')
    password = request.GET.get('password')
    email = request.GET.get('email')
    type = request.GET.get('type')
    if username and password:
        if len(username)<6:
            return HttpResponse("用户名长度小于6")
        if len(password)<6:
            return HttpResponse("密码长度小于6")
    else:
        return HttpResponse("用户名密码为空")
    u=User(username=username,password=make_password(password),email=email,first_name=name,last_name=type)#pt表示普通用户，qy表示企业用户
    try:
        u.save()
    except:
        return HttpResponse("已存在的用户名")

    login(request,u)
    return HttpResponse("注册成功")

def forgotPasswd(request):
    email = User.objects.get(username=request.user).email
    from django.core.mail import send_mail
    import random
    code=random.randint(1000,9999)
    send_mail(
        'Subject here',
        "code is "+str(code),
        '15610575692@163.com',
        [email],
        fail_silently=False,
    )
    return HttpResponse('您的密码已发送到您的邮件')

def changePaawd(request):
    username = request.user
    password = request.POST.get('password')
    User.objects.fiter(username=username).update(password=make_password(password))
    return HttpResponse("修改成功")










def regC(request):#先注册用户账号，然后注册公司
    if request.user.is_authenticated:
        u=User.objects.get(username=request.user)
    else:
        return HttpResponse("未注册用户账号")

    name = request.GET.get('name')
    type = request.GET.get('type')
    ps = request.GET.get('ps')
    info = request.GET.get('info')
    tel = request.GET.get('tel')


    return HttpResponse("注册成功")