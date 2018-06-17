# coding:utf-8
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from order.serializers import  *
from order.models import Order,DishRecord
from dishes.toolset import getStartEnd,isRegCustomer
#from pandas.plotting._tools import table
# Create your views here.


#获取count，即数量
#根据不同user类型返回不同的数量
#返回的json格式
'''
{
	"count":12
}
'''
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




#获取没有完成的订单的count，即数量，
#厨师端专用
#返回的json格式
'''
{
	"count":12
}
'''
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getUnfinishedOrderCount(request):
    res = Order.objects.filter(finished=False).count()
    serial = {'count':res}
    return Response(serial)








#获取取消掉的订单的count，即数量，
#厨师端专用
#返回的json格式
'''
{
	"count":12
}
'''
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getCancelOrderCount(request):
    res = Order.objects.filter(cancel=True).count()
    serial = {'count':res}
    return Response(serial)





#获取没有完成的订单，返回的是详细的订单信息
#厨师端专用
'''
格式
[
 {
    "id" :2,
    "username"  :"anon",
    "price" :12.8,
    "finished" :True,
    "cancel" :False,
    "note"  :"shiiiit",
    "table"  :3
 },....
]
'''
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))
def getUnfinishedOrder(request):
    res = Order.objects.filter(finished=False,cancel=False)
    serial = DetailOrderSerializer(res,many=True)
    return Response(serial.data)





#获取单个订单的信息，需要订单id为参数
'''
format:
{
    "id" :2,
    "username"  :"anon",
    "price" :12.8,
    "finished" :True,
    "cancel" :False,
    "note"  :"shiiiit",
    "table"  :3
}
'''
@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def OneOrderInfo(request,orderid):
    try:
        res = Order.objects.get(id=orderid)
        serial_order = DetailOrderSerializer(res,many=False)
        return Response( serial_order.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)





#获取订单下所有菜的信息，需要订单id为参数
'''
format:
[
 {
    "orderID" :1,
    "dishID" :2,
    "number":2,
    "price" :12
    "finished":True
 },...
]
'''

@api_view(['GET'])
@authentication_classes((SessionAuthentication, ))
def getDishRecord(request, order):
    #获取一个订单的所有菜
    res = DishRecord.objects.filter(orderID=order)      
    serial = DetailDishRecordSerializer(res,many=True)
    return Response(serial.data)












#下面的函数会根据参数吧结果分页并给出所需的那一页，一般用于目录，所以不会获取所有信息
'''
[
   {
      "id" :2,
      "price" :12,
      "finished" :True,

	},...
]
'''
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










#点餐发送订单，create是创建，cancel是取消
'''
request data format
{
type:'create'   or   'cancel'
order:  Order json with cancel  == true or false
dishrecord: [dishr1,dishr2...]
}


返回格式，-1的话说明失败或者该桌子还没结账
{"orderID": 1121}
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
    
    if request.session.get('table'):
        tableNum = request.session['table']
    else:
        tableNum = data['order']['table']
    
    
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
            newdr.number = x['number']
            newdr.price = x['price']
            newdr.finished = False
            newdr.save()
        return Response({'orderID',orderID},status=status.HTTP_201_CREATED)
    
    
    
#staff才可以用的方法，把某订单勾选为完成
#返回值为{"orderID":111},可以不用理会           
@api_view(['POST'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))            
def finishOrder(request):
	data=request.data
	orderID = data['orderID']
	Order.objects.filter(orderID = orderID).update(finished = True)
	DishRecord.objects.filter(orderID =orderID).update(finished = True)
	return Response({'orderID',orderID},status=status.HTTP_201_CREATED)




#完成单道菜
#返回值为{"orderID":111},可以不用理会
@api_view(['POST'])
@authentication_classes((SessionAuthentication, ))
@permission_classes((IsAdminUser,))            
def finishDish(request):
	data=request.data
	orderID = data['orderID']
	dishID = data['dishID']
	DishRecord.objects.filter(orderID =orderID,dishID=dishID).update(finished = True)
	return Response({'orderID',orderID},status=status.HTTP_201_CREATED)



    
