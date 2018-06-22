# coding:utf-8
import uuid
from django.db import models

# Create your models here.
class Table(models.Model):
    uuid = models.UUIDField('专属字符串',default=uuid.uuid4,editable=False)
    occupy = models.BooleanField('是否使用中')
    
    def __str__(self):
        return '桌面'+str(self.id)