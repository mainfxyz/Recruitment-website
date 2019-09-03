from django.shortcuts import render,HttpResponse
from django.views.generic.list import ListView
import sys
sys.path.append("..")
from ZpModel.models import Zp,CV,CV2Zp,Com
from django.db.models import Q
import re
from functools import reduce
import operator
from django.contrib.auth.models import User

def page_not_found(request):
    return render(request,'404.html')

def loginfo(request):
    user = request.user
    if user != None and user != "" and not user.is_anonymous:
        context = '<i class="fa fa-user-circle" style="font-size:19px"></i>&nbsp' + str(user) + '</a>' \
                '&nbsp&nbsp&nbsp<a class="text-white" id="logout"> <i class="fa fa-sign-out" style="font-size:19px"></i>注销'
    else:
        context = '<i class="fa fa-sign-in" style="font-size:19px"></i>&nbsp&nbsp<span>登录</span>'
    return context


def me(request):
    context = {}
    context['user'] = loginfo(request)

    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        try:
            cv = CV.objects.get(user_id=u.id)
            context['name'] = u.first_name
            context['sex'] = cv.sex
            context['age'] = cv.age
            context['edu'] = cv.edu
            context['tc'] = cv.super
            context['jn'] = cv.tech
            context['tel'] = cv.tel
            context['email'] = u.email
            context['sal1'] = cv.K1
            context['sal2'] = cv.K2
            context['workingExp']=cv.exp
            context['wantJob']=cv.wantJob
            context['school']=cv.school
            context['gzjl']=cv.gzjl
            context['jybj'] = cv.jybj
            context['zwjs']=cv.zwjs
            for k in context.keys():
                if context[k]==None:
                    context[k]=""
        except:
            if u.last_name == 'pt':
                cv = CV(user_id=u.id)
                cv.save()
            else:
                return ZpListView.as_view()(request)
    else:#如果没有登录就返回注册
        return register(request)
    return render(request,'me.html',context)

def submit_me(request):
    context = {}
    if not request.user.is_authenticated:
        return register(request)

    user = request.GET.get('user')
    sex = request.GET.get('sex')
    edu = request.GET.get('edu')
    age = request.GET.get('age')
    super = request.GET.get('tc')
    tech = request.GET.get('jn')
    tel = request.GET.get('tel')
    email = request.GET.get('email')
    K1 = request.GET.get('sal1')
    K2 = request.GET.get('sal2')
    exp = request.GET.get('workingExp')
    wantJob = request.GET.get('wantJob')
    school= request.GET.get('school')
    gzjl = request.GET.get('gzjl')
    jybj = request.GET.get('jybj')
    zwjs = request.GET.get('zwjs')

    u = User.objects.get(username=request.user)
    cv = CV.objects.get(user_id=u.id)
    cv.age = age if age or None else None

    if exp or None:#None 和 ""都不执行
        cv.exp = exp
    else:
        cv.exp=None
    if K1 or None:
        cv.K1=K1
    else:
        cv.K1=None
    if K2 or None:
        cv.K2 = K2
    else:
        cv.K2=None
    cv.sex = sex
    cv.edu=edu
    cv.super=super
    cv.tech=tech
    cv.tel=tel
    u.email=email
    cv.wantJob=wantJob
    cv.school=school
    cv.gzjl=gzjl
    cv.jybj=jybj
    cv.zwjs=zwjs
    cv.save()

    u.first_name=user
    u.save()
    return me(request)


def register(request):
    context = {}
    context['user'] = loginfo(request)
    return render(request,'register.html',context)

















class ZpListView(ListView):
    we=""
    edu=""
    job=""
    salary=""
    path=""
    search=""
    user = "登录"
    model = Zp#数据源
    template_name = "index.html"#网页链接
    paginate_by = 10  # if pagination is desired，分页每页的信息条数

#修改查询数据
    def get_queryset(self):
        d={"edu1":"大专","edu2":"本科","edu3":"硕士","edu4":"博士","edu5":"不限",
           "job1":"教育","job2":"互联网","job3":"管理","job4":"文秘","job5":"电子","job6":"机械","job7":"客服","job8":"销售",
           "job9":"银行","job10":"保险","job11":"汽车","job12":"采购","job13":"化工","job14":"设计",
           "we1":[1,3],"we2":[3,5],"we3":[5,10],"we4":[10,100],
           "sa1":[0,3],"sa2":[3,5],"sa3":[5,10],"sa4":[10,30],"sa5":[30,1000],"sa6":[0,0]}
        r=Zp.objects.all()
        #搜索框
        try:
            self.search=re.match('/list_(.*)',self.path).group(1)
            r = r.filter(jobName__contains=self.search)
        except:
            pass
        #教育等级
        if self.edu!=None and self.edu!="":
            edus=self.edu.split('_')
            eduLevel = [d[x] for x in edus if x in d.keys()]
            if len(eduLevel)==1:
                r = r.filter(eduLevel=eduLevel[0])
            elif len(eduLevel)==0:
                pass
            else:
                r=r.filter(eduLevel__in=eduLevel)
        #工作领域
        if self.job!=None and self.job!="":
            jobs=self.job.split('_')
            jobType = [d[x] for x in jobs if x in d.keys()]
            try:
                r=r.filter(reduce(operator.or_, map(lambda x: Q(jobType__contains=x), jobType)))
            except:
                pass
        #薪资
        if self.salary!=None and self.salary!="":
            k=[]
            for x in self.salary.split('_'):
                if x in d.keys():
                    k.append(d[x])
            r = r.filter(reduce(operator.or_, map(lambda x: Q(K1__gte=x[0]) & Q(K2__lte=x[1]), k)))
        #经验
        if self.we!=None and self.we!="":
            k=[]
            for x in self.we.split('_'):
                if x in d.keys():
                    k.append(d[x])
            r = r.filter(reduce(operator.or_, map(lambda x: Q(W1__gte=x[0]) & Q(W2__lte=x[1]), k)))
        return r

#添加返回数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user!=None and self.user!="" and not self.user.is_anonymous:
            context['user']='<i class="fa fa-user-circle" style="font-size:19px"></i>&nbsp'+str(self.user)+'</a>' \
                '&nbsp&nbsp&nbsp<a class="text-white" id="logout"> <i class="fa fa-sign-out" style="font-size:19px"></i>注销'
        else:
            context['user'] = '<i class="fa fa-sign-in" style="font-size:19px"></i>&nbsp&nbsp<span>登录</span>'
        return context

#获取request
    def get(self, request, *args, **kwargs):
        self.we = request.GET.get('we')
        self.edu = request.GET.get('edu')
        self.job = request.GET.get('job')
        self.salary = request.GET.get('salary')
        self.path = request.path
        self.user = request.user
        r=super().get(self, request, *args, **kwargs)
        return r


def CVgo(request):
    user=request.user
    if not user.is_authenticated:
        return HttpResponse(status=403,content='请登录')
    zpId=request.GET.get('zpId')
    com_id=Zp.objects.get(id=zpId).com_id
    jobName = request.GET.get('jobName')
    cv2zp=CV2Zp(zp_id=zpId,user_id=user.id)
    cv2zp.jobName=jobName
    cv2zp.email=user.email
    cv2zp.name=user.first_name
    cv2zp.com_id=com_id
    try:
        CV.objects.get(user_id=user.id)
    except:
        return HttpResponse("请完善简历")
    try:
        cv2zp.save()
    except:
        return HttpResponse(content="不能重复投递")
    return HttpResponse('OK')