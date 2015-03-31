#coding=utf-8
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from notesite import settings
import os.path
import datetime

import json
#把某一个文件保存到本地
def saveToFile(path,value):
    f = file(path,'wb')
    f.flush()
    f.write(value)
    f.close()

def getError(msg):
    return json.dumps({"error":1,"message":msg})


#for upload img


def upload_img(request):
    #文件保存目录路径
    savePath = settings.ATTACHED_PATH
    #文件保存目录URL
    saveUrl = "/static/attached/"
    #允许上传的文件扩展名
    fileTypes = ['gif','jpg','jpeg','png','bmp']
    #最大文件大小
    maxSize = 1000000

    if request.FILES:
        #save path is exist
        if not os.path.exists(savePath):
            return HttpResponse(getError("upload dir not exist!"))

        for item in request.FILES:
             #check file size is not bigger than maxSize
            if request.FILES[item].size > maxSize:
                return HttpResponse(getError("upload file'size is too big!"))
            fileExt = os.path.splitext(request.FILES[item].name)[1].lower().lstrip('.')
            if fileExt not in fileTypes:
                return HttpResponse(getError("not support file type!"))
            ttuple = datetime.datetime.now().timetuple()
            tstr = ("".join(str(t) for t in ttuple))[0:-2]
            newFileName = tstr + "-" + request.FILES[item].name
            try:
                saveToFile(newFilePath,request.FILES[item].read())
            except:
                return HttpResponse(getError("can't save file! upload failed!"))


            #success,return json msg
            jstr = json.dumps({"error":0,"url":saveUrl+newFileName})
            return HttpResponse(jstr)
    return HttpResponse(getError("not file upload! select a file please!"))
            







        
            
        
