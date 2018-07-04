# coding:utf-8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dishes.toolset import getStartEnd
from dishes.serializers import *
from dishes.models import *





#根据dish id获取菜的详情
'''
{
    "id":2,
    "name" :"anon",
    "price":23.7,
    "dtype": "sichuan",
    "description":"gioog",
    "pic":"/img/uploads/xxx.jpg",
    "recommend": False
}
'''
@api_view(['GET'])
def getOneDishInfo(request, dishid):
    try:
        res = Dishes.objects.get(id=dishid,soldout=False)
        serial = DetailDishSerializer(res,many=False)
        return Response(serial.data)
    except Dishes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


#获得所有菜的信息
'''
[
    {
    "id":2,
    "name" :"anon",
    "price":23.7,
    "dtype": "sichuan",
    "description":"gioog",
    "pic":"/img/uploads/xxx.jpg",
    "recommend": False
    }
]
'''
@api_view(['GET'])
def getAllDishInfo(request):
    res = Dishes.objects.filter(soldout=False)
    serial = DetailDishSerializer(res,many=True)
    return Response(serial.data)


#获取菜类别信息
'''
[
    {"dtype":"noodles"},
    {"dtype":"rubbish"}
]
'''
@api_view(['GET'])
def getCategoryInfo(request):
    res = Category.objects.all()
    serial = DetailCategorySerializer(res,many=True)
    return Response(serial.data)




# Create your views here.
