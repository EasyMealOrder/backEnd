# coding:utf-8
from rest_framework import serializers
from order.models import  DishRecord,Order

class DetailDishRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishRecord
        exclude = ('id')
        
     
class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'


class SimpOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = ('id','price','finished')