from django.http import HttpResponse         #需要导入HttpResponse模块
from django.shortcuts import render
from django.shortcuts import render_to_response
from Free import getUrlFromInternet
from django.http import HttpResponseRedirect
def hello(request):                          #request参数必须有，名字类似self的默认规则，可以修改，它封装了用户请求的所有内容
    return HttpResponse("Hello world ! ")    #不能直接字符串，必须是由这个类封装，此为Django规则

def viewMovie(request):
    # return HttpResponse("Hello world ! ")
    context = {}
    context['hello'] = 'Hello World!'  # 数据绑定
    context['v_url'] = 'https://tbm.alicdn.com/6vAsJsegVeBeb6vz3Vi/QoblkUutvdRvp882djB@@hd.m3u8'  # 默认初始影片地址
    return render(request, 'test.html',context)  #  将绑定的数据传入前台
    # return render_to_response('demo2.htm')

# 接收请求数据
def search(request):
    context = {}
    request.encoding='utf-8'
    if 'q' in request.GET:
        message=getU(request.GET['q'])
        if 'm3u8' in message:
            context['v_url'] = message
        else:
            context['v_url_mp4'] = message
    else:
        return HttpResponse('there is no url !! are you kidding me?')
    return render(request, 'test.html',context)  # 将绑定的数据传入前台

def getU(sourse_u):
    print(sourse_u)
    # sourse_u = 'http://m.iqiyi.com/v_19rr7pmvcw.html'
    # https://hao.czybjz.com//ppvod/E2B089E0CC627E27D6F095CF364D801D.m3u8
    return getUrlFromInternet.getVideoUrl(sourse_u)
