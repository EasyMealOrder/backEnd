# coding:utf-8
from rest_framework import serializers
from statistic.models import Feedback,Statistic

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        field = '__all__'
        
class DetailFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        field = '__all__'
