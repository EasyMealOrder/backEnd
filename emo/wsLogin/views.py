# coding:utf-8
from django.shortcuts import render,HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from wsLogin.models import WxUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json
import random
import string

# Create your views here.
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
            return HttpResponseNotFound()
    
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

    '''
    try:
        existUser = WxUser.objects.get(session_id=session)
        responseData = {'openid': existUser.id, 'nickname': existUser.nickname, 'sex': existUser.sex, 'province': existUser.province, 'city': existUser.city, 'country': existUser.country, 'headimgurl': existUser.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    except BaseException:
        user = WxUser()
        user.sex = random.randint(1,2)
        user = user.save()
        user.session_id = session 
        user.nickname = 'user'+str(user.id)
        user.province = 'province'+str(user.id)
        user.city = 'city'+str(user.id)
        user.country = 'country'+str(user.id)
        user.headimgurl = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1529751764221&di=7b77ae9d0598a1d996abbd83ff63b7b5&imgtype=0&src=http%3A%2F%2Fupload.mnw.cn%2F2018%2F0324%2F1521876947374.png'
        user = user.save()
        responseData = {'openid': user.id, 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    '''