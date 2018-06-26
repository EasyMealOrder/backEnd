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


@api_view(['POST'])
@csrf_exempt
def wxLogin(request):
    #value = ''
    #try:
    #    value = request.COOKIES["sessionid"]
    #except BaseException:
    #    value = ''
    if request.user.is_authenticated:
        cUser = request.user
        print(cUser)
        csrf(request)
        try:
            #print(csrf(request))
            #existUser = User.objects.get(username=cUser.username)
            userOpenid = WxOpenid.objects.get(openid=cUser.username)
            addr = 'http://0.0.0.0:9000/fakewx?openid='+userOpenid.openid+'&access_token='+userOpenid.access_token
            #流程
            strRes = readJsonFrom(addr)
            js = json.loads(strRes)
            return Response(js)
        except WxOpenid.DoesNotExist:
            return Response({'detail':'No this openid'})
        except BaseException:
            return Response({'detail':'wrong openid or access_token pos 1'})
        
    else:
        try:
            openid = request.POST["openid"]
        except BaseException:
            return Response({'opneid':''})

        try:
            access_token = request.POST["access_token"]
        except BaseException:
            return Response({'access_token':''})

        addr = 'http://0.0.0.0:9000/fakewx?openid='+openid+'&access_token='+access_token
        #流程
        strRes = readJsonFrom(addr)
        if strRes == None:
            return Response({'detail':'wrong openid or access_token'})
        #print(type(json))
        js = json.loads(strRes)
        try: 
            userOpenid = WxOpenid.objects.get(openid = openid)
            userOpenid.access_token = access_token
            userOpenid.save()
            user = User.objects.get(username = openid)
            print(user)
            login(request,user)
            return Response(js)
        except WxOpenid.DoesNotExist:
            userOpenid = WxOpenid()
            userOpenid.openid = openid
            userOpenid.access_token = access_token
            userOpenid.save()

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


@api_view(['GET'])
@csrf_exempt
def fakeWx(request):
    try:
        openid = request.GET['openid']
    except BaseException:
        print(2222)
        return Response({'openid':''})
    
    try:
        user = WxUser.objects.get(session_id=openid)
        print(444)
        responseData = {'openid': openid, 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        #print(responseData)
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    except WxUser.DoesNotExist:
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
    