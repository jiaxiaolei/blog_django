#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from models import Pic

from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from forms import RegisterForm,LoginForm,PiclistForm,PwdupdateForm


#photo
import settings
import os.path
import datetime

# 分页 modual

from django.shortcuts import render_to_response
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

# 定义各种各样的函数  

# 首页视图 （到一个欢迎界面  welcome.html）
def index(request):
    '''首页视图'''
    template_var={"w":_(u"您好，欢迎使用python测试系统!")}
    if request.user.is_authenticated():
        template_var["w"]=_(u"欢迎您 %s!")%request.user.username
    return render_to_response("accounts/welcome.html",template_var,context_instance=RequestContext(request))

# 注册视图 （到注册界面 register.html）
def register(request):
    '''注册视图'''
    template_var={}
    form = RegisterForm()    
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=User.objects.create_user(username,email,password)
            user.save()
            _login(request,username,password)#注册完毕 直接登陆
            return HttpResponseRedirect(reverse("index"))    
    template_var["form"]=form        
    return render_to_response("accounts/register.html",template_var,context_instance=RequestContext(request))
    
# 登陆视图 （到一个登陆界面 login.html ）
def login(request):
    '''登陆视图'''
    template_var={}
    form = LoginForm()    
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            return HttpResponseRedirect(reverse("index"))
    template_var["form"]=form        
    return render_to_response("accounts/login.html",template_var,context_instance=RequestContext(request))
    
#  点击登陆按钮提交之后调用的方法， 给出一些反馈信息 
def _login(request,username,password):
    '''登陆核心方法'''
    ret=False
#  自己定义的 uthenticate 判断权限的方法 
    user=authenticate(username=username,password=password)

# 如果存在  
    if user:
        if user.is_active:
            auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))

# 如果不存在 
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))

# 默认 ret 为 false  
    return ret

# 点击注销，退出系统     
def logout(request):
    '''注销视图'''
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


   
#  上传图片   （到一个 上传图片的界面  picupload.html ）
def saveToFile(path,value):
    f = file(path,'wb')
    f.flush()
    f.write(value)
    f.close()


# 把数据保存到数据表中    ？？？？？  
def picupload(request):
     '''上传图片'''
     savePath = settings.ATTACHED_PATH
     saveUrl = "/static/attached/"

     fileTypes = ['gif','jpg','jpeg','png','bmp']

     maxSize = 1000000

     if request.FILES:
         if not os.path.exists(savePath):
             return HttpResponseRedirect(reverse('index'))

         for item in request.FILES:
           
             fileExt = os.path.splitext(request.FILES[item].name)[1].lower().lstrip('.')
             ttuple = datetime.datetime.now().timetuple()
             tstr = ("".join(str(t) for t in ttuple))[0:-2]
             newFileName = tstr + "-" + request.FILES[item].name
             newFilePath = savePath + newFileName
             saveToFile(newFilePath,request.FILES[item].read())

             # 保存图片信息
             pic=Pic(path=newFilePath,username=request.user.username,time=str(datetime.datetime.now())[0:20])
             pic.save()

             
             return HttpResponseRedirect(reverse('index'))
     return render_to_response("accounts/picupload.html",context_instance=RequestContext(request))
## 跳转到 上传图片界面
## 提交 -----------------


  
#   修改密码   （ 判断前后面目是否相等两个到一个 ）
def pwdupdate(request):
    '''修改密码界面'''
    template_var={}
    form = PwdupdateForm()    
    if request.method == 'POST':
        form=PwdupdateForm(request.POST.copy())
        if form.is_valid():           
            password=form.cleaned_data["newpwd1"]
            password2=form.cleaned_data["newpwd2"]
            if password==password2:
                if request.user.is_authenticated():
                    user = User.objects.get(username=request.user.username)
                    user.set_password(password)
                    user.save()
                return HttpResponseRedirect(reverse("index"))
            messages.add_message(request, messages.INFO, _(u'两次输入的密码不一致，请重新输入'))
            return HttpResponseRedirect(reverse("pwdupdate"))
    template_var["form"]=form        
    return render_to_response("accounts/pwdupdate.html",template_var,context_instance=RequestContext(request))

    

#  图片列表   （到一个 显示图片列表的界面  piclist.html ）
def piclist(request):
    '''图片列表'''
    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page======',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    info = Pic.objects.order_by('id').all()
    paginator = Paginator(info,3)

    try:
        picList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        picList = paginator.page(1)
    #– 显示范围 –#
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response("accounts/piclist.html",locals())


#  查看帮助   （到一个 显示图片列表的界面  help.html ）
def help(request):
    '''查看帮助''' 
     #      
    return render_to_response("accounts/help.html")
 



#  查看人员列表   （到一个 显示图片列表的界面  help.html ）
def  userlist(request):
    '''查看人员列表'''
    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page======',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    info = User.objects.order_by('id').all()
    paginator = Paginator(info,6)

    try:
        picList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        picList = paginator.page(1)
    #– 显示范围 –#
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response("accounts/userlist.html",locals())
 




    



