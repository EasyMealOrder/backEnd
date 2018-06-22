# coding:utf-8
from rest_framework import serializers
from frontpage.models import Table

class DetailTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        field = '__all__'
        exclude = ()
        