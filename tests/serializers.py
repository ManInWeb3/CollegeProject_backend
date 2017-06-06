from rest_framework import serializers
from .models import TestLog, Test
import datetime
from django.utils import timezone


class TestLogSerializer(serializers.ModelSerializer):
    """
    Serializing testlog table
    """
    # screenshot = serializers.ImageField(required=False,allow_empty_file=True,)
    # photo = serializers.ImageField(required=False,allow_empty_file=True,)
    # text =  serializers.CharField(required=False,)
    class Meta:
        model = TestLog
        fields = '__all__'
       # fields = ('id', 'screenshot', 'photo', 'datetime', 'text', 'test_id')

class TestSerializer(serializers.ModelSerializer):
    """
    Serializing Test table
    """
    class Meta:
        model = Test
        fields = '__all__'
