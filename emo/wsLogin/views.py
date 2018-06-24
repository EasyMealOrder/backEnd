# coding:utf-8
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from wsLogin.models import WxUser
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


def readJsonFrom(addr):
    try:
        response =  urllib.request.urlopen(addr)
        html = response.read()
        html = html.decode('utf-8')
        json = json.loads(html)
        return json
    except BaseException:
        return None

@api_view(['POST'])
def wxLogin(request):
    #value = ''
    #try:
    #    value = request.COOKIES["sessionid"]
    #except BaseException:
    #    value = ''
    try:
        session = request.POST["session_id"]
    except BaseException:
        return Response({'opneid':''})


    if request.user.is_authenticated:
        cUser = request.user
        try:
            existUser = User.objects.get(username=cUser.username)
            return Response({'openid':cUser.username})
        except BaseException:
            return Response({'openid':''})
        
    else:
        addr = 'http://0.0.0.0:8000/fakewx/'+session+'/'
        #流程
        json = readJsonFrom(addr)
        if json == None:
            return Response({'openid':''})
        un = json.openid
        try: 
            user = User.objects.get(username=un)
            login(request,user)
            return Response(json)
        except User.DoesNotExist:
            randomPass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            default_user=User.objects.create_user(username=un,password=randomPass)  #创建新用户 
            login(request,default_user)
            return Response(json)

        '''
        readJsonFrom访问api网站
        返回一个object，或者None，None的话说明出错了
        以这个Object的openid字段来查找User的username，若有，就把它登陆并返回信息
        没有就创建，并登陆，返回信息
        记得异常处理
        '''


@api_view(['POST'])
def fakeWx(request,session_id):
    try:
        session = session_id
    except BaseException:
        return Response({'opneid':''})
    try:
        user = WxUser.objects.get(session_id=session)
        responseData = {'openid': str(user.id), 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return Response(responseData)
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
        responseData = {'openid': str(user.id), 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return Response(responseData)
    except BaseException:
        return Response({'opneid':''})
    