# coding:utf-8
from rest_framework import serializers
from dishes.models import *


class DetailDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        exclude = ('soldout')
        

class SimpDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        exclude = ('soldout','description')
        

class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = '__all__'
        
