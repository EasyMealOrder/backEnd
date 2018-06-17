# coding:utf-8
from django.db import models

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('用户名', max_length=150)
    price=models.FloatField('价格')    
    finished=models.BooleanField('是否完成')
    cancel=models.BooleanField('是否取消')
    note = models.TextField('标注')
    table = models.IntegerField('桌号')
    
    
    def __str__(self):
        return '订单号'+str(self.id)

class DishRecord(models.Model):
    orderID = models.BigIntegerField('订单号')
    dishID = models.IntegerField('菜编号')
    number = models.IntegerField('数量')
    price = models.FloatField('价格')
    finished=models.BooleanField('是否完成')
    
    def __str__(self):
        return str(self.orderID) + " - >" + str(self.dishID)
