from django.db import models

# Create your models here.
class WxUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_id = models.CharField('session_id', max_length=150)
    nickname = models.CharField('昵称', max_length=150)
    sex = models.IntegerField('性别')    
    province = models.CharField('省份', max_length=150)
    city = models.CharField('城市', max_length=150)
    country = models.CharField('城市', max_length=150)
    headimgurl = models.CharField('头像', max_length=150)
    privilege = models.CharField('特权', max_length=150)
    unionid = models.CharField('统一标识', max_length=150)