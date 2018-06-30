#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Statistic(models.Model):
    dish = models.CharField('菜名',max_length = 256)
    sold = models.IntegerField('卖出')
    
    def __str__(self):
        return self.dish+"统计"
    
    
class Feedback(models.Model):
    orderID = models.BigIntegerField('订单编号', primary_key=True)
    star = models.FloatField('星级')
    comment = models.TextField('评价')
    username = models.CharField('用户名', max_length=150)
    
    def __str__(self):
        return '反馈'+str(self.orderID)