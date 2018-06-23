from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
    
@csrf_exempt
def auth_view(request):
    username=request.POST.get("username")       # 获取用户名
    password=request.POST.get("password")       # 获取用户的密码
    try:
        print(type(username))
        print(type(password))
    except BaseException:
        return Response({'success',False})
    
    try:
        user=authenticate(username=username,password=password)  # 验证用户名和密码，返回用户对象
        
        if user:                        # 如果用户对象存在
            login(request,user)         # 用户登陆
            resp = {'success': True, 'detail': 'login success!'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        
        else:
            resp = {'success': False, 'detail': 'user doesn\'t exist or the password is wrong!'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    except BaseException:
        return Response({'orderID',-4})
@csrf_exempt
def logout_view(request):
    if not request.user.is_authenticated:
        resp = {'success': False, 'detail': "authentication fail!"}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), \
        content_type="application/json")
        
    logout(request)     # 注销用户
        
    resp = {'success': True, 'detail': 'logout success!'}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
  
@csrf_exempt
def create_user(request):
    
    msg=""
    
    if request.method=="POST":
        username=request.POST.get("username"," ")           # 获取用户名，默认为空字符串
        password=request.POST.get("password"," ")           # 获取密码，默认为空字符串
        confirm=request.POST.get("confirm_password"," ")    # 获取确认密码，默认为空字符串
    
        if password == "" or confirm=="" or username=="":   # 如果用户名，密码或确认密码为空
            msg="用户名或密码不能为空"
        elif password !=confirm:                            # 如果密码与确认密码不一致
            msg="两次输入的密码不一致"
        elif User.objects.filter(username=username):        # 如果数据库中已经存在这个用户名
            msg=username+"该用户名已存在"
        else:
            new_user=User.objects.create_user(username=username,password=password)  #创建新用户 
            new_user.save()
            
            resp = {'success': True, 'detail': 'create user success!'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        
    resp = {'success': False, 'detail': msg}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def change_passwd(request):
    if not request.user.is_authenticated:
        resp = {'success': False, 'detail': "authentication fail!"}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), \
        content_type="application/json")

    user=request.user       # 获取用户名
    msg=None
    
    if request.method=='POST':
        old_password=request.POST.get("old_password","")    # 获取原来的密码，默认为空字符串
        new_password=request.POST.get("new_password","")    # 获取新密码，默认为空字符串
        confirm=request.POST.get("confirm_password","")     # 获取确认密码，默认为空字符串

        if user.check_password(old_password):               # 到数据库中验证旧密码通过
            if not new_password or not confirm:                     # 新密码或确认密码为空
                msg="新密码不能为空"   
            elif new_password != confirm:                   # 新密码与确认密码不一样
                msg="两次密码不一致"
    
            else:
                user.set_password(new_password)             # 修改密码
                user.save()
                resp = {'success': True, 'detail': 'change password success!'}
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

        else:
            msg="旧密码输入错误"

    resp = {'success': False, 'detail': msg}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")