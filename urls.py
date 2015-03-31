#coding=utf-8

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^level_1/', include('level_1.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

# 相当于 java 中的配置文件    定义所有的actiion  和跳转    url 的第一个参数竟然是正则
#   设置默认的开始页

    url(r'^$', 'accounts.views.index',name="index"),
    url(r'^accounts/index$', 'accounts.views.index',name="accounts_index"),
    url(r'^accounts/register$', 'accounts.views.register',name="register"),
    url(r'^accounts/login$', 'accounts.views.login',name="login"),
    url(r'^accounts/logout$', 'accounts.views.logout',name="logout"),
    url(r'^accounts/picupload$', 'accounts.views.picupload',name="picupload"),
    url(r'^accounts/pwdupdate$', 'accounts.views.pwdupdate',name="pwdupdate"),
    url(r'^accounts/piclist$', 'accounts.views.piclist',name="piclist"),
    url(r'^accounts/help$', 'accounts.views.help',name="help"),
    url(r'^accounts/userlist$', 'accounts.views.userlist',name="userlist"),                       
    url(r'^accounts/static/attached/(?P<path>.*)$','django.views.static.serve',{'document_root':'./static/attached'})
    

)
