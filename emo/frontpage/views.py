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
def assignTable(request,table):
    
    if request.session.get('table'):
        
        if request.session['table'] != table:
            return HttpResponseRedirect('/table/'+request.session['table']+'/')
            
        #render front page
        try:
            Table.objects.get(uuid=table)
            return HttpResponse('Welcome !  You have old session, table uuid is'+ table)
        except BaseException:
            return HttpResponseNotFound('no such table')

    else:
        try:
            Table.objects.get(uuid=table)
            request.session['table'] = table
            return HttpResponse('Welcome !  You have new session, table uuid is'+ table)
        except BaseException:
            return HttpResponseNotFound('no such table')
        
        
        #render front page
        return HttpResponse('Welcome !  You are new, table id is'+str(table))


def testSession(request):
    if request.session.get('table'):
        return HttpResponse('Welcome !  You already have session, table uuid is'+request.session['table'])
    else:
        return HttpResponse('No session')


@api_view(['GET'])
def getTables(request):
    res = Table.objects.all()
    serial = DetailTableSerializer(res,many=True)
    return Response(serial.data)