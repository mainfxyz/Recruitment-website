"""zpWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import view,account,bigDataView,cViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.ZpListView.as_view()),
    re_path(r'^list_.*', view.ZpListView.as_view()),
    path('login',account.logIN),
    path('logout',account.logOUT),
    path('reg',account.reg),
    path('register',view.register),
    #path('forgot',account.forgotPasswd),
    path('me',view.me),
    path('submit_me',view.submit_me),

    path('view',bigDataView.v),
    path('tj',bigDataView.match_CV.as_view()),
    path('jlpp',bigDataView.jl),
    path('collection',bigDataView.v),

    #path('j_main',bigDataView.j_main),

    #公司部分
    path('cIndex',cViews.cIndex),
    path('cAppli',cViews.cAppli.as_view()),
    path('saveComInfo/', cViews.save_com_info),
    path('addZp', cViews.addZp),
    path('saveZp',cViews.saveZp),
    path('delZp',cViews.delZp),
    path('CVgo', view.CVgo),
    path('lookCV',cViews.lookCV),
    # path('refuse',cViews.refuse),
    # path('send',cViews.send)
]
