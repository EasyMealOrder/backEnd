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

'''
返回格式
{
	count:1
}
'''
# Create your views here.
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def getFeedbackCount(request):
	res = Feedback.objects.all().count()
	serial = {'count':res}
	return Response(serial)



'''
返回格式
{
	"orderID":2,
	"star":4,
	"comment":"xxx",
	"username":"anon"
}
'''   
#feedback由order确定，一个order只能有一个feedback 
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def getOneFeedbackInfo(request,orderid):
    try:
        res = Feedback.objects.get(orderID=orderid)
        serial = DetailFeedbackSerializer(res,many=False)
        return Response(serial.data)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

'''
输入：/一页项目数量/第几页/
返回格式
[
	{
	"orderID":2,
	"star":4,
	"comment":"xxx",
	"username":"anon"
	},

	{
	"orderID":3,
	"star":4,
	"comment":"xdxx",
	"username":"anon"
	}
]
'''
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def getManyFeedbackInfo(request, numOfOnePage, page):
    count = Feedback.objects.all().count()
    if count == 0:
        return Response([])
    start,end = getStartEnd(count,numOfOnePage, page)
    if start == -1:
        return Response([])
    res = Feedback.objects.all()[start:end]
    serial = DetailFeedbackSerializer(res,many=True)
    return Response(serial.data)

'''
输入：
{
	"orderID":2,
	"star":3,
	"comment":"xxxxxx"
}
输出：
{
	"orderID":2
}
出错orderID返回为负数
'''
@api_view(['POST'])
@authentication_classes((SessionAuthentication, ))
def setFeedback(request):
	data = request.data
	try:
		fb = Feedback.objects.get(orderID = data['orderID'])
		fb.star = data['star']
		fb.comment = data['comment']
		fb.save()
		return Response({'orderID':fb.orderID})
	except BaseException:
		return Response({'orderID':-1})
