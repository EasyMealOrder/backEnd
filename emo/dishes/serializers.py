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
        
        
class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'

class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = '__all__'
        
class SimpOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = ('id','price','finished')
        
        
class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        field = '__all__'
        
class DetailFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        field = '__all__'

        
class SimpFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        field = ('oderID','star')  
