import requests
import time
import execjs

import re
import json

Mainurl = 'https://api.47ks.com/webcloud/?v='+'http://www.iqiyi.com/v_19rr7pgf14.html'
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
def md5(num):
    ctx = execjs.compile(getJs("md5"))
    return ctx.call('md5', num)
def getMainJs():
    headers = {
        'Host': 'api.47ks.com',
        'User-Agent': UserAgent,
        'Referer': 'http://mmore.xyz/',
        'Upgrade-Insecure-Requests': '1'
    }
    r = requests.get(Mainurl,headers=headers)
    # f = open('./js/file', 'w', encoding='UTF-8')
    # f.write(r.text)
    return r.text
    # f = open('./js/file', 'r', encoding='UTF-8')
    # line = f.readline()
    # jsstr = ''
    # while line:
    #     jsstr = jsstr + line
    #     line = f.readline()
    # return jsstr
def snatchVideoUrl(k,k2,k3,ep,cip,cip_hex,csign,tm,v,pt,nip,from_,mode):
    # 先固定referer 完善后再修改
    headers = {
               'Host': 'api.47ks.com',
               'User-Agent': UserAgent,
               'Referer': Mainurl,
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Accept': 'application/json,text/javascript,*/*;q=0.01',
               'X-Requested-With': 'XMLHttpRequest'                     #这个必须加上，不然会无法得到正确结果
    }
    postdata = {
                'k': k,
                'k2': k2,
                'k3': k3,
                'ep': ep,
                'cip': cip,
                'cip_hex': cip_hex,
                'csign': csign,
                'tm': tm,
                'v': v,
                'pt': pt,
                'nip': nip,
                'from': from_,
                'mode': mode
                }
    # print(headers)
    # # postdata = json.dumps(postdata)
    # print(postdata)
    req = requests.post("https://api.47ks.com/config/webmain.php", data=postdata, headers=headers)
    # req.encoding = 'utf-8'  # 显式地指定网页编码，一般情况可以不用
    # print(req.headers['content-type'])
    # print(req.encoding)
    # print(req.apparent_encoding)

    # print(req.text)
    videoUrlJson = req.text
    # # 如果用firfox浏览器直接输入，需要将几个带有百分号等的参数变换一下
    # ctx = execjs.compile(getJs("md5"))
    # k3 = ctx.call('encodeURIComponent', k3)
    # v = ctx.call('encodeURIComponent', v)
    # from_ = ctx.call('encodeURIComponent', from_)
    # ep = ctx.call('encodeURIComponent', ep)
    # print('k=' + k + '&k2=' + k2 + '&k3=' + k3 + '&ep=' + ep + '&cip=' + cip + '&cip_hex=' + cip_hex + '&csign=' + csign + '&tm=' + tm + '&v=' + v + '&pt=' + pt + '&nip=' + nip + '&from=' + from_ + '&mode=' + mode)
    return videoUrlJson
def getEp(url):
    headers = {
                'Host': 'kr.47ks.com',
                'User-Agent': UserAgent,
                'Referer': Mainurl,
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
               }
    r = requests.get(url,headers=headers)
    return r.text
# 获取js文件中的内容
def getJs(name):
    jsurl = "static/js/"+name+".js"
    f = open(jsurl, 'r', encoding='UTF-8')
    line = f.readline()
    jsstr = ''
    while line:
        jsstr =jsstr + line
        line = f.readline()
    return jsstr

# 获取k , k2 ,k3 等参数.
def getParametersAndUrl():
    # 方便起见，md5xp中的内容以及player中起作用的部分已经复制到了md5中
    tm = 0
    cache = 0
    k_3 = 0
    k_4 = 0
    vd = 0
    k = 0
    k2 = 0
    k3 = 0
    ep = 0
    cip = 0
    cip_hex = 0
    v = 0
    mode = ""
    pt = "auto"
    nip = 'null'
    from_ = 'http://mmore.xyz/'

    # 这里获取 可推到出k 的某数
    str = getMainJs()
    tm = str[str.find('"tm" value="', 0, len(str))+12:str.find('"tm" value="', 0, len(str))+22]
    # print("tm:  " + tm)
    cache = str[str.find('cache = ', 0, len(str))+8:str.find('cache = ', 0, len(str))+18]
    # print("cache:  "+cache)
    k_secondparam = str[str.find('vd +',0,len(str))+5:str.find('vd +',0,len(str))+39]  # "k的第二个参数 "
    k_secondparam = k_secondparam[1:len(k_secondparam)-1]
    # print("k的第二个参数 "+k_secondparam)

    ctx = execjs.compile(getJs("md5"))
    k_3 = ctx.call('md5', cache)
    k_4 = ctx.call('md5', k_3)
    # print('k_4 = '+k_4)
    # vd = ctx.call('md5', (k_3+k_4))

    #真实k_3以及vd
    temporary = str.find('eval("',0,len(str))
    eval_string = str[temporary:str.find('")',temporary,len(str))+3]
    # print(eval_string)
    # print(len(eval_string))
    # print(eval_string.find('x27',0,len(eval_string)))
    # print(eval_string.find('x27',eval_string.find('x27',0,len(eval_string))+1,len(eval_string)))
    eval_k3 = eval_string[eval_string.find('x27',0,len(eval_string))-1:eval_string.find('x27',eval_string.find('x27',0,len(eval_string))+1,len(eval_string))+3]
    eval_vd = eval_string[eval_string.find('x27',eval_string.find('x27',eval_string.find('x27',0,len(eval_string))+1,len(eval_string))+1,len(eval_string))-1:eval_string.find('x27',eval_string.find('x27',eval_string.find('x27',eval_string.find('x27',0,len(eval_string))+1,len(eval_string))+1,len(eval_string))+1,len(eval_string))+3]
    # print(eval_k3)
    # print(eval_vd)
    eval_k3 = '"'+eval_k3+'"'
    k_3_ = eval(eval_k3)
    k_3 = k_3_[1:len(k_3_)-1]
    # print(' k_3 = '+ k_3)
    eval_vd = '"'+eval_vd+'"'
    vd_ = eval(eval_vd)
    vd = vd_[1:len(vd_)-1]
    # print('vd = '+ vd)

    # 这里通过解密找到cache的新值，以及k_4的新算出方法,解密方式见博客
    cache = '2384843'
    # k_4 = md5(cache.toString()+vd.toString()+document.domain+md5('41d785ff9079cee021d2bb9d715f7582'))
    k_4 = md5(cache+vd+'api.47ks.com'+md5('41d785ff9079cee021d2bb9d715f7582'))
    k = ctx.call('md5x',(vd+k_secondparam))
    k2 = ctx.call('md5',k_3)
    k3 = ctx.call('encodeURIComponent',ctx.call('get',k_4))
    # print("k = "+k+'    k2 = '+k2+"      k3 = "+k3)
    # 准备获取ep
    ep_url_f = str[str.find('getep?k=',0,len(str)):str.find('getep?k=',0,len(str))+360]
    ep_url = "https://kr.47ks.com/Info/getep?k"+ep_url_f[7:ep_url_f.find('"',0,len(ep_url_f))]
    # ep_url = 'https://kr.47ks.com/Info/getep?k=YjQwYWs2S1U3bDg0VUhhdGtLRkM2RCUyQkhmR2N5TFNVUUJkZEFmVGcwUUVnTHFhSEJwZG5DYUVoQzd2YjRSR2F4TmxWZjRwWHJRJTJCT244S01wYmtmNmRGJTJCZ240WCUyQlpzJTJGNnYlMkZvVldOS3JHSWRrQlM5ank5c0IlMkZ2b0d3SEN4c2I4cGVBNTNrdDBLcmRTbG40S1F4ajFzb3FaQXVCb090SFJ1QUJCbXhIdGJNbTNzWEJsJTJCOHlpUm4xN3VlbFBKMlRhaFclMkJKMVplcGVzWkQyT3cwV3phWnIlMkZSY2swZW8='
    # print('ep_url = '+ep_url)
    ep_text = getEp(ep_url)
    # print(ep_text)
    ep = ep_text[ep_text.find('"',0,len(ep_text))+1:ep_text.find('"',30,len(ep_text))]
    # print("这里得到了ep其中 ep = "+ep)
    # 大多参数都是从此句中取出的，因此将其单独列出来，代替str，减小时空开销
    post_str = str[str.find('$.post(', 0, len(str)):str.find('},', str.find('$.post(', 0, len(str)), len(str)) + 1]
    # print('post_str = ' + post_str)
    cip = post_str[post_str.find('"cip"',0,len(post_str))+8:post_str.find('"cip_hex"',0,len(post_str))-2]
    cip_hex = post_str[post_str.find('"cip_hex"',0,len(post_str))+12:post_str.find('"csign"',0,len(post_str))-2]
    csign = str[str.find('id="get"', 0, len(str)) + 16:str.find('"',str.find('id="get"', 0, len(str))+18,len(str))]
    # print('csign = ' +csign )
    v = post_str[post_str.find('"v":',0,len(post_str))+6:post_str.find('",',post_str.find('"v":',0,len(post_str)),len(post_str))]
    # print('v = '+ v)
    # return k,k2,k3,ep,cip,cip_hex,csign,tm,v,pt,nip,from_,mode

    return snatchVideoUrl(k,k2,k3,ep,cip,cip_hex,csign,tm,v,pt,nip,from_,mode)
def getParameterTM():
    tm = int(time.time())*3-26641
    # print(tm)
    return tm

def getVideoUrl(sourse_url):
    global Mainurl
    Mainurl = 'https://api.47ks.com/webcloud/?v=' + sourse_url
    videoUrlJson = getParametersAndUrl()
    # 将 JSON 对象转换为 Python 字典
    videoUrlJson = json.loads(videoUrlJson)
    # print(videoUrlJson['play'])
    videoUrl = videoUrlJson['url']
    # print(videoUrlJson['success'])
    print(videoUrl)
    return videoUrl
# if __name__ == "__main__":
#     getVideoUrl('http://www.iqiyi.com/v_19rr7pgf14.html#vfrm=19-9-0-1')