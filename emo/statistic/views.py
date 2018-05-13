# coding:utf-8
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from statistic.serializers import  *
from statistic.models import Feedback
from dishes.toolset import getStartEnd
# Create your views here.
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getFeedbackCount(request):
    res = Feedback.objects.all().count()
    serial = {'count':res}
    return Response(serial)
   
#feedback由order确定，一个order只能有一个feedback 
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getOneFeedbackInfo(request,orderid):
    try:
        res = Feedback.objects.get(orderID=orderid)
        serial = DetailFeedbackSerializer(res,many=False)
        return Response(serial.data)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getManyFeedbackInfo(request, numOfOnePage, page):
    count = Feedback.objects.all().count()
    start,end = getStartEnd(count,numOfOnePage, page)
    if start == -1:
        return Response(status=status.HTTP_404_NOT_FOUND)
    res = Feedback.objects.all()[start:end]
    serial = DetailFeedbackSerializer(res,many=True)
    return Response(serial.data)
