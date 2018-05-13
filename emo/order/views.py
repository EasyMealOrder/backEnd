# coding:utf-8
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from order.serializers import  *
from order.models import Order
from dishes.toolset import getStartEnd
# Create your views here.


#获取count，即数量
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAuthenticated,))
def getOrderCount(request):
    user = request.user
    if user.is_staff == False:
        res = Order.objects.filter(username=user.username).count()
    else:
        res = Order.objects.all().count()
    serial = {'count':res}
    return Response(serial)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAuthenticated,))
def getUnfinishedOrderCount(request):
    user = request.user
    if user.is_staff == False:
        res = Order.objects.filter(finished=False,username=user.username).count()
    else:
        res = Order.objects.filter(finished=False).count()
    serial = {'count':res}
    return Response(serial)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAuthenticated,))
def OneOrderInfo(request,orderid):
    try:
        res = Order.objects.get(id=orderid).order_by('-id')
        serial_order = DetailOrderSerializer(res,many=False)
        rec = DishRecord.obejects.filter(orderID=orderid)
        serial_rec = DetailDishRecordSerializer(rec,many=True)
        return Response({'orderInfo':serial_order.data,'records':serial_rec.data})
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


#下面的函数会根据参数吧结果分页并给出所需的那一页，一般用于目录，所以不会获取所有信息
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAuthenticated,))
def getManyOrderInfo(request, numOfOnePage, page):
    user = request.user
    if user.is_staff == False:
        count = Order.objects.filter(username=user.username).count()
        start,end = getStartEnd(count,numOfOnePage, page)
        if start == -1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        res = Order.objects.filter(username=user.username).only('id','price','finished').order_by('-id')[start:end]
    else:
        count = Order.objects.all().count()
        start,end = getStartEnd(count,numOfOnePage, page)
        if start == -1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        res = Order.objects.all().only('id','price','finished').order_by('-id')[start:end]
    serial = SimpOrderSerializer(res,many=True)
    return Response(serial.data)


'''
request data format
{
type:'create'   or   'cancel'
order:  Order json with cancel  == true or false
dishrecord: [dishr1,dishr2...]
}
'''
@api_view(['POST'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAuthenticated,))
def ccOrderInfo(request):
    #cc means create and cancel
    #
    data = request.data
    if data['type'] == 'create':
        neworder = Order()
        neworder.username = request.user.username
        neworder.price = data['order']['price']
        neworder.finished = data['order']['finished']
        neworder.cancel=False
        neworder.note=data['order']['note']
        neworder = neworder.save()
        orderID = neworder.id
        for x in data['dishrecord']:
            newdr = DishRecord()
            newdr.dishID = x['dishID']
            newdr.orderID=orderID
            newdr.name = x['name']
            newdr.number = x['number']
            newdr.price = x['price']
            newdr.save()
        return Response({'orderID',orderID})
    if data['type'] == 'cancel' :
        orderID = data['order']['id']
        Order.objects.filter(id=orderID).update(cancel=True)
           
            
    
    
