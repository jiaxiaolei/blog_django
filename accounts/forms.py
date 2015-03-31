#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# 这里仅仅是定义标签#    注册from类  
class RegisterForm(forms.Form):
  
    username=forms.CharField(label=_(u"用户名"),max_length=30,widget=forms.TextInput(attrs={'size': 30,}))
    password=forms.CharField(label=_(u"密  码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 30,}))
    email=forms.EmailField(label=_(u"邮  箱"),max_length=30,widget=forms.TextInput(attrs={'size': 30,}))    
    
    # 使用类库验证 是否重复
    def clean_username(self):
        '''验证重复昵称'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"  该用户名已经被使用，请重新输入"))
        
    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"该邮箱已经被使用，请重新输入"))

#   登陆类        
class LoginForm(forms.Form):
    username=forms.CharField(label=_(u"用户名"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"密  码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))


#   图片列表 类      国际化中  设置界面标签     输入框等在froms.py 文件中都能设置 
class PiclistForm(forms.Form):
    label=forms.CharField(label=_(u"上传图片"))
    time=forms.CharField(label=_(u"上传时间"))
    name=forms.CharField(label=_(u"上传人"))



#     修改密码  类  
class PwdupdateForm(forms.Form):    
    newpwd1=forms.CharField(label=_(u"新   密  码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    newpwd2=forms.CharField(label=_(u"再次确认密码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    
