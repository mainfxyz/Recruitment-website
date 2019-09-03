import sys
sys.path.append("..")
from ZpModel.models import Zp,Com,CV
from django.shortcuts import render
from . import olap
from .view import loginfo
from .view import ZpListView,me
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.http import Http404

def j_main(request):
    j={}
    j['line1']=olap.W1()
    return JsonResponse(j)



def v(request):
    context={}
    context['user']=loginfo(request)

    #数据计算
    #r=Zp.objects.filter()
    # r=Zp.objects.filter()
    #
    context['data1'],context['data2'],context['data3']=olap.K2()
    context['line1']=olap.W1()

    return render(request, 'view.html', context)

def jl(request):
    try:
        return match_CV.as_view()(request)
    except:
        return me(request)


class match_CV(ZpListView):
    template_name = 'match_CV.html'

    def get_queryset(self):
        u=User.objects.get(username=self.user)
        cv = CV.objects.get(user_id=u.id)
        K1=cv.K1
        K2=cv.K2
        exp=cv.exp
        edu=cv.edu
        jobName=cv.wantJob

        edus=[]
        for e in ['大专','本科','硕士','博士']:
            if edu==e:
                edus.append(e)
                break
            else:
                edus.append(e)
        try:
            r=Zp.objects.filter(Q(K1__gte=K1),Q(K2__lte=K2),Q(W1__lte=exp))
            r=r.filter(Q(jobType__contains=jobName)|Q(jobName__contains=jobName))
            r=r.filter(eduLevel__in=edus)
        except:
            raise Exception
        #jobType edu
        return r