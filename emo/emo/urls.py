# coding:utf-8
from django.conf import settings 
from django.conf.urls.static import static
from django.conf.urls import include


"""emo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dishes import views as dishes_api
from order import views as order_api
from statistic import views as sta_api
from frontpage import views as frp_api
from login import views as login_api
from websocket import views as ws_api

urlpatterns = [
    path('test/', frp_api.testSession,name='testSession'),           #test session
    path('<int:table>/', frp_api.assignTable,name='assigntable'),
    path('admin/', admin.site.urls),
    path('dish/',dishes_api.getAllDishInfo,name="getAllDishInfo"),
    path('dish/<int:dishid>/',dishes_api.getOneDishInfo,name="getOneDishInfo"),
    path('category/',dishes_api.getCategoryInfo,name="getCategoryInfo"),
    path('order/count/',order_api.getOrderCount,name="getOrderCount"),
    path('order/<int:orderid>/',order_api.OneOrderInfo,name="OneOrderInfo"),
    path('order/pages/<int:numOfOnePage>/<int:page>/',order_api.getManyOrderInfo,name="getManyOrderInfo"),
    path('feedback/count',sta_api.getFeedbackCount,name="getFeedbackCount"),
    path('feedback/<int:orderid>/',sta_api.getOneFeedbackInfo,name="getOneFeedbackInfo"),
    path('feedback/pages/<int:numOfOnePage>/<int:page>/',sta_api.getManyFeedbackInfo,name="getManyFeedbackInfo"),
    path('signup/',login_api.create_user,name="createUser"),
    path('signin/',login_api.auth_view,name="createUser"),
    path('signout/',login_api.logout,name="createUser"),
    path('changePass/',login_api.change_passwd,name="createUser"),
    path('index2/',ws_api.index2),
    path('echo/',ws_api.echo),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  