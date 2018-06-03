from django.shortcuts import render
from django.http.response import HttpResponse


#”√session±Íº«
# Create your views here.
def assignTable(request,table):
    
    if request.session.get('table'):
        if request.session['table'] != table:
            request.session['table'] = table
            
        #render front page
        return HttpResponse('Welcome !  You already have session, table id is'+str(table))
    else:
        request.session['table'] = table
        
        
        #render front page
        return HttpResponse('Welcome !  You are new, table id is'+str(table))


def testSession(request):
    if request.session.get('table'):
        return HttpResponse('Welcome !  You already have session, table id is'+str(request.session['table']))
    else:
        return HttpResponse('No session')