# coding:utf-8
from rest_framework import serializers
from dishes.models import *


class DetailDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        exclude = ('soldout')
        field = '__all__'
        

class SimpDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        exclude = ('soldout','description')
        field = '__all__'
        

class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()
        field = '__all__'
        
