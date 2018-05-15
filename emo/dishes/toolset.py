# coding:utf-8
from django.contrib.auth.models import Group




#paging all the items
#input  Model, the number of items that one page contains,  page number
#return start, end,      you can using in slice
#For example:  Feedback.objects.all().only('orderID','star')[start:end]
#if out of range, return -1,-1
def getStartEnd(count, numOfOnePage, page):
    if numOfOnePage*page-numOfOnePage >= count:
        return -1,-1
    if numOfOnePage < 1 or page < 1:
        return -1,-1
    start = numOfOnePage*(page-1)
    end = count  if numOfOnePage*page > count else numOfOnePage*page
    return start,end



#确定用户是不是在消费者群组中

def isRegCustomer(user):
    group = Group.objects.get(name='customers')
    if group in user.groups.all():
        return True
    else:
        return False