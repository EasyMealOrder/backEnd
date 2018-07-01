# 写一下返回的json格式


## Order

返回的OrderRecord，OrderRecord是Order相关的一条条记录，由（orderID,dishID）标记，附带的还价格和数量

```
{
    "orderID" :1,
    "dishID" :2,
    "number":2,
    "price" :12
    "finished":True
}
```

返回的详细的Order，用订单id查询才会返回这么详细的order，匿名用户的username是"anon"：
```
{
    "id" :2,
    "username"  :"anon",
    "price" :12.8,
    "finished" :True,
    "cancel" :False,
    "note"  :"shiiiit",
    "table"  :3
}
```


如果请求多个order，返回的是这些，主要是给目录显示：
```
{
    "id" :2,
    "price" :12,
    "finished" :True,

}
```


## dish
详细的dish信息，用dish的id查询才能得到：
```
{
    "id":2,
    "name" :"anon",
    "price":23.7,
    "dtype": "sichuan",
    "description":"gioog",
    "pic":"/img/uploads/xxx.jpg",
    "recommend": False
}
```

获取全部dish信息，会给你没详细描述的json
```
{
    "id":12,
    "name" :"trr",
    "price":12,
    "dtype": "no",
    "pic":"/img/uploads/xxxx.jpg",
    "recommend" :True
}
```

## Feedback
反馈吧，我也不知道有用没用。用orderID查询可以得到
```
{
    "orderID":2,
    "star":4.5,
    "comment":"no...",
    "username":"anon"
}
```
