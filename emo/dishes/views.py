# coding:utf-8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dishes.toolset import getStartEnd
from dishes.serializers import *
from .models import *
from django.http.response import JsonResponse
import json


@api_view(['GET'])
def getOneDishInfo(request, dishid):
    try:
        res = Dishes.objects.get(id=dishid,soldout=False)
        serial = DetailDishSerializer(res,many=False)
        return Response(serial.data)
    except Dishes.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getAllDishInfo(request):
    res = Dishes.objects.filter(soldout=False).defer('soldout','description')
    serial = SimpDishSerializer(res,many=True)
    return Response(serial.data)

@api_view(['GET'])
def getCategoryInfo(request):
    res = Category.objects.all()
    serial = DetailCategorySerializer(res,many=True)
    return Response(serial.data)



@api_view(['GET'])
def getOrderCount(request):
    res = Order.objects.all().count()
    serial = {'count':res}
    return Response(json.dumps(serial))


@api_view(['GET'])
def getOneOrderInfo(request,orderid):
    try:
        res = Order.objects.get(id=orderid)
        serial = DetailOrderSerializer(res,many=False)
        return Response(serial.data)
    except Order.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getManyOrderInfo(request, numOfOnePage, page):
    start,end = getStartEnd(Order,numOfOnePage, page)
    if start == -1:
        return Response(status.HTTP_404_NOT_FOUND)
    res = Order.objects.all().only('id','price','finished')[start:end]
    serial = SimpOrderSerializer(res,many=True)
    return Response(serial.data)

@api_view(['GET'])
def getOneFeedbackInfo(request,orderid):
    try:
        res = Feedback.objects.get(orderID=orderid)
        serial = DetailFeedbackSerializer(res,many=False)
        return Response(serial.data)
    except Feedback.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getManyFeedbackInfo(request, numOfOnePage, page):
    start,end = getStartEnd(Feedback,numOfOnePage, page)
    if start == -1:
        return Response(status.HTTP_404_NOT_FOUND)
    res = Feedback.objects.all().only('orderID','star')[start:end]
    serial = SimpFeedbackSerializer(res,many=True)
    return Response(serial.data)


# Create your views here.
