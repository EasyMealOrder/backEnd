from django.shortcuts import render,HttpResponse
import json
import random

# Create your views here.
def login(request):
    session = request.POST.get("session_id")
    existUser = WxUser.objects.get(session_id=session)
    if existUser == None:
        user = WxUser()
        user = user.save()
        user.session_id = session 
        user.nickname = 'user'+str(user.id)
        user.sex = random.randint(1,2)
        user.province = 'province'+str(user.id)
        user.city: user.city, '' = 'city'+str(user.id)
        user.country = 'country'+str(user.id)
        user.headimgurl = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1529751764221&di=7b77ae9d0598a1d996abbd83ff63b7b5&imgtype=0&src=http%3A%2F%2Fupload.mnw.cn%2F2018%2F0324%2F1521876947374.png'
        user = user.save()
        responseData = {'openid': user.id, 'nickname': user.nickname, 'sex': user.sex, 'province': user.province, 'city': user.city, 'country': user.country, 'headimgurl': user.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")
    else:
        responseData = {'openid': existUser.id, 'nickname': existUser.nickname, 'sex': existUser.sex, 'province': existUser.province, 'city': existUser.city, 'country': existUser.country, 'headimgurl': existUser.headimgurl, 'privilege': '超级加倍', 'unionid': '3838438'}
        return HttpResponse(json.dumps(responseData, ensure_ascii=False), content_type="application/json")

    