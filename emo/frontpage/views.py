#coding:utf-8
from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from frontpage.models import Table
from frontpage.serializers import DetailTableSerializer
#分配桌子
# Create your views here.
@api_view(['GET'])
def assignTable(request,table):
    
    try:
        tableObj = Table.objects.get(id=table)
    except BaseException:
        return Response({"table":-1})
    

    if tableObj.occupy == True:
        return Response({"table":-2})
    
    return Response({"table":table})


@api_view(['GET'])
def getTables(request):
    res = Table.objects.all()
    serial = DetailTableSerializer(res,many=True)
    return Response(serial.data)