# coding:utf-8
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.serializers import  *
from order.models import Order
from dishes.toolset import getStartEnd,isRegCustomer
from pandas.plotting._tools import table
# Create your views here.


#获取count，即数量
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def getOrderCount(request):
    user = request.user
    if user.is_staff == True:
        res = Order.objects.all().count()
    elif isRegCustomer(user):
        res = Order.objects.filter(username=user.username).count()
    else:
        res = 1
    serial = {'count':res}
    return Response(serial)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getUnfinishedOrderCount(request):
    res = Order.objects.filter(finished=False).count()
    serial = {'count':res}
    return Response(serial)



@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getCancelOrderCount(request):
    res = Order.objects.filter(cancel=True).count()
    serial = {'count':res}
    return Response(serial)



@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
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
def getManyOrderInfo(request, numOfOnePage, page):
    user = request.user
    
    #注册用户会返回属于他的订单
    if isRegCustomer(user):
        
        count = Order.objects.filter(username=user.username).count()
        start,end = getStartEnd(count,numOfOnePage, page)
        if start == -1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        res = Order.objects.filter(username=user.username).only('id','price','finished').order_by('-id')[start:end]
        
    #staff用户会返回所有的订单    
    elif user.is_staff:
        
        
        count = Order.objects.all().count()
        start,end = getStartEnd(count,numOfOnePage, page)
        if start == -1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        res = Order.objects.all().only('id','price','finished').order_by('-id')[start:end]
        
     #匿名用户只返回一个最新的订单，桌号根据session来获取 
    else:
        if request.session.get('table',default=None):
            res = Order.objects.filter(table=int(request.session['table'])).order_by('-id')[0:1]  
        else:
            return Response([])
        
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
def ccOrderInfo(request):
    #cc means create and cancel
    data = request.data
    
    if data['type'] == 'cancel' :
        orderID = data['order']['id']
        Order.objects.filter(id=orderID).update(cancel=True)
        return Response(status=status.HTTP_200_OK)
    
    session_table = int(request.session['table']) if request.session.get('table', 0) else -1
    
    #如果没告知,用session的table号
    tableNum = data['order']['table'] if data['order']['table'] >= 0 else session_table
    
    #如果都没有,返回负数订单号，表示出错了
    if tableNum == -1:
        return Response({'orderID',-1},status=status.HTTP_204_NO_CONTENT)
    
    if Order.objects.filter(table=tableNum).count() != 0:
        lastestOder = Order.objects.filter(table=tableNum).order_by('-id')[0]
        #订单进行中,却有针对同一桌新订单出现，返回负数订单号
        if lastestOder.cancel == False and lastestOder.finished == False:
            return Response({'orderID',-1},status=status.HTTP_204_NO_CONTENT)
            
    if data['type'] == 'create':
        neworder = Order()
        neworder.username = request.user.username if request.user.username != '' else 'anon'
        neworder.price = data['order']['price']
        neworder.finished = data['order']['finished']
        neworder.table=tableNum
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
        return Response({'orderID',orderID},status=status.HTTP_201_CREATED)
    
    
    
           
            
    
    
