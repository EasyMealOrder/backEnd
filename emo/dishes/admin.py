# coding:utf-8
from django.contrib import admin
from dishes.models import Dishes
from dishes.models import Category



admin.site.register(Dishes)
admin.site.register(Category)
#admin.site.register(Order)
# Register your models here.