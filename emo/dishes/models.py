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
    recommend = models.BooleanField('是否推荐')        #discount or someting?
    
    def __str__(self):
        return self.name
 

