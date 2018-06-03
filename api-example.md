#写一下返回的json格式


##Order

返回的OrderRecord，OrderRecord是Order相关的一条条记录，由（orderID,dishID）标记，附带的还价格和数量

'''
{
    "orderID" :
    "dishID" :
    "number":
    "price" :
}
'''     

返回的详细的Order，用订单id查询才会返回这么详细的order，匿名用户的username是"anon"：
'''
{
    "id" :
    "username"  :
    "price" :
    "finished" :
    "cancel" :
    "note"  :
    "table"  :
}
'''


如果请求多个order，返回的是这些，主要是给目录显示：
'''
{
    "id" :
    "price" :
    "finished" :

}
'''


## dish
详细的dish信息，用dish的id查询才能得到：
'''
{
    "id":
    "name" :
    "price":
    "dtype": 
    "description":
    "pic":
    "recommend" :
}
'''

获取全部dish信息，会给你没详细描述的json
'''
{
    "id":
    "name" :
    "price":
    "dtype": 
    "pic":
    "recommend" :
}
'''

##Feedback
反馈吧，我也不知道有用没用。。用orderID查询可以得到
'''
{
    "orderID":
    "star":
    "comment":
    "username":
}
'''

##  Statistic
没啥用。。。没想用来干嘛
