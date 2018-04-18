# coding:utf-8
from django.db import models
# Create your models here.


# The category of dishes
class Category(models.Model):
    dtype = models.CharField('类型',max_length = 256,primary_key=True)
    
    def __str__(self):
        return self.dtype
    
#一道菜的详情
class Dishes(models.Model):
    name = models.CharField('菜名',max_length = 256)
    price = models.FloatField('价格')
    dtype = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    description = models.TextField('描述')
    pic = models.ImageField('图片',upload_to='img')
    soldout = models.BooleanField('是否售空')
    recommend = models.BooleanField('是否推荐')        #discount
    
    def __str__(self):
        return self.name
 
 
 #以下的Model都是为了记录信息创建的，不要注册到admin管理界面   
#订单详情
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    dishes=models.TextField('菜名表')
    discount = models.FloatField('折扣')
    price=models.FloatField('应付')    
    finished=models.BooleanField('是否完成')
    note = models.TextField('备注')
    
    
    def __str__(self):
        return '订单编号：'+self.id


class Statistic(models.Model):
    dish = models.CharField('菜名',max_length = 256)
    sold = models.IntegerField('售出数量')
    
    def __str__(self):
        return self.dish+"统计信息"
    
    
class Feedback(models.Model):
    orderID = models.BigIntegerField('对应订单编号', primary_key=True)
    star = models.FloatField('星级')
    comment = models.TextField('评价')
    
    def __str__(self):
        return '订单号： '+self.orderID+'评价'