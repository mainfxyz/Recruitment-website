from django.contrib import admin
from .models import Zp,Com,CV
# Register your models here.
admin.site.site_title="招聘网站后台"
admin.site.site_header="后台管理"
admin.site.index_title="欢迎登陆"

class ZpAdmin(admin.ModelAdmin):
    list_display = ('jobName','company','eduLevel','K1','K2','W1','W2')

class ComAdmin(admin.ModelAdmin):
    list_display = ('name','tel','email','type','ps')

class CVAdmin(admin.ModelAdmin):
    list_display = ('user_id','sex','age','edu','super','tech')

admin.site.register(Zp,ZpAdmin)
admin.site.register(Com,ComAdmin)

admin.site.register(CV,CVAdmin)