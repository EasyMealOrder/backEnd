from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse


@accept_websocket
def echo(request):
    if request.is_websocket():#判断是不是websocket连接
        count = Order.obejects.all().count()
        while True:
            if request.websocket.has_messages():
                #deal with message 
                #if client request an abort
                #then break
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
            
def index2(request):
    return render(request, 'index.html')