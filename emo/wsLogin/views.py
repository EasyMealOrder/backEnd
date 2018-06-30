# coding:utf-8
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from wsLogin.models import WxUser, WxOpenid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json
import random
import string
import urllib.request

# Create your views here.
"""
@csrf_exempt
def wxLogin(request):
    #value = ''
    #try:
    #    value = request.COOKIES["sessionid"]
    #except BaseException:
    #    value = ''

    if request.user.is_authenticated:
        cUser = request.user
        try:
            existUser = WxUser.objects.get(session_id=cUser.username)
        except BaseException:
            return HttpResponse(json.dumps({'openid':''}, ensure_ascii=False), content_type="application/json")
        responseData = {'openid': str(existUser.id), 'nickname': existUser.nickname, 'sex': existUser.sex, 'province': existUser.province, 'city': existUser.city, 'country': existUser.country, 'headimgurl': existUser.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    else:
        ######假微信#####
        try:
            session = request.POST["session_id"]
        except BaseException:
            return HttpResponse(json.dumps({'openid':''}, ensure_ascii=False), content_type="application/json")
    
        try:
            user = WxUser.objects.get(session_id=session)
            default_user = User.objects.get(username=session)
            login(request,default_user)
            responseData = {'openid': str(user.id), 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
            return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
        except WxUser.DoesNotExist:
            user = WxUser()
            user.sex = random.randint(1,2)
            user.save()
            user.session_id = session 
            user.nickname = 'user'+str(user.id)
            user.province = 'province'+str(user.id)
            user.city = 'city'+str(user.id)
            user.country = 'country'+str(user.id)
            user.headimgurl = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1529751764221&di=7b77ae9d0598a1d996abbd83ff63b7b5&imgtype=0&src=http%3A%2F%2Fupload.mnw.cn%2F2018%2F0324%2F1521876947374.png'
            user.save()
            randomPass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            default_user=User.objects.create_user(username=session,password=randomPass)  #创建新用户 
            login(request,default_user)
            responseData = {'openid': str(user.id), 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
            return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
        except BaseException:
            return HttpResponse(json.dumps({'openid':''}, ensure_ascii=False), content_type="application/json")
"""

#访问url,response转换成json返回
@csrf_exempt
def readJsonFrom(addr):
    try:
        response =  urllib.request.urlopen(addr)
        html = response.read()
        html = html.decode('utf-8')
        #print(html)
        return html
    except BaseException:
        return None

#假装微信登录
@api_view(['POST'])
@csrf_exempt
def wxLogin(request):
    #value = ''
    #try:
    #    value = request.COOKIES["sessionid"]
    #except BaseException:
    #    value = ''
    #如果request带sessionid,验证用户
    if request.user.is_authenticated:
        cUser = request.user
        print(cUser)
        #csrf校验
        csrf(request)
        try:
            #print(csrf(request))
            #existUser = User.objects.get(username=cUser.username)
            #获取用户
            userOpenid = WxOpenid.objects.get(openid=cUser.username)
            #访问假装微信接口
            addr = 'http://0.0.0.0:9000/fakewx?openid='+userOpenid.openid+'&access_token='+userOpenid.access_token
            #流程
            strRes = readJsonFrom(addr)
            #加载为json
            js = json.loads(strRes)
            return Response(js)
        except WxOpenid.DoesNotExist:
            return Response({'detail':'No this openid'})
        except BaseException:
            return Response({'detail':'wrong openid or access_token pos 1'})
        
    else:
        #没有sessionid,获取POST form-data格式数据
        try:
            openid = request.POST["openid"]
        except BaseException:
            return Response({'opneid':''})

        try:
            access_token = request.POST["access_token"]
        except BaseException:
            return Response({'access_token':''})
        #访问假装微信接口获取用户信息
        addr = 'http://0.0.0.0:9000/fakewx?openid='+openid+'&access_token='+access_token
        #流程
        strRes = readJsonFrom(addr)
        if strRes == None:
            return Response({'detail':'wrong openid or access_token'})
        #print(type(json))
        js = json.loads(strRes)
        try: 
            #用户openid若在本地数据库存在,更换access_token
            userOpenid = WxOpenid.objects.get(openid = openid)
            userOpenid.access_token = access_token
            userOpenid.save()
            #获取openid对应的用户系统的用户并登陆
            user = User.objects.get(username = openid)
            print(user)
            login(request,user)
            return Response(js)
        except WxOpenid.DoesNotExist:
            #openid在本地数据库不存在,创建WxOpenid对象保存openid,access_token
            userOpenid = WxOpenid()
            userOpenid.openid = openid
            userOpenid.access_token = access_token
            userOpenid.save()
            #用户系统注册用户,密码随机生成并登录
            randomPass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            default_user=User.objects.create_user(username=openid,password=randomPass)  #创建新用户 
            login(request,default_user)
            return Response(js)

            

        '''
        readJsonFrom访问api网站
        返回一个object，或者None，None的话说明出错了
        以这个Object的openid字段来查找User的username，若有，就把它登陆并返回信息
        没有就创建，并登陆，返回信息
        记得异常处理
        '''

#假装微信接口
@api_view(['GET'])
@csrf_exempt
def fakeWx(request):
    try:
        #获取openid
        openid = request.GET['openid']
    except BaseException:
        print(2222)
        return Response({'openid':''})
    
    try:
        #openid已存在,假装微信获取用户信息并返回
        user = WxUser.objects.get(session_id=openid)
        print(444)
        responseData = {'openid': openid, 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        #print(responseData)
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    except WxUser.DoesNotExist:
        #openid不存在本地数据库,创建假微信用户
        #随机生成用户信息并返回用户信息
        user = WxUser()
        user.sex = random.randint(1,2)
        user.save()
        user.session_id = openid 
        user.nickname = 'user'+str(user.id)
        user.province = 'province'+str(user.id)
        user.city = 'city'+str(user.id)
        user.country = 'country'+str(user.id)
        user.headimgurl = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1529751764221&di=7b77ae9d0598a1d996abbd83ff63b7b5&imgtype=0&src=http%3A%2F%2Fupload.mnw.cn%2F2018%2F0324%2F1521876947374.png'
        user.save()
        responseData = {'openid': openid, 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        #print(responseData)
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    except BaseException:
        print(333)
        return Response({'opneid':''})
    