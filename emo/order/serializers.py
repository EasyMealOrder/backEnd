# coding:utf-8
from rest_framework import serializers
from order.models import  DishRecord,Order
from dishes.models import Dishes

class DetailDishRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishRecord
        exclude = ('id',)
        
     
class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'
        exclude = ()


class SimpOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ()
        field = ('id','price','finished')

class DetailDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        exclude = ('soldout',)
        field = '__all__'
