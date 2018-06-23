from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
from order.models import Order
from order.serializers import DetailOrderSerializer


@accept_websocket
def echo(request):
    print(1)
    if request.is_websocket():#判断是不是websocket连接
        count = Order.obejects.all().count()
        while True:
            if request.websocket.has_messages():
                print(1)
            else:
                newcount = Order.obejects.all().count()
                if count !=  newcount:
                    res = Order.objects.filter(finished = False)[count,newcount]
                    serial_order = DetailOrderSerializer(res,many=True)
                    request.websocket.send(serial_order.data)
                
                #check database
                #if new order occurs
                #send new order to clients
            sleep(5)
            