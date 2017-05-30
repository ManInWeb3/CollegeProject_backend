from rest_framework import serializers
from .models import TestLog, Test
import datetime
from django.utils import timezone


class TestLogSerializer(serializers.ModelSerializer):
    """
    Serializing testlog table
    """
#    ivr_id = serializers.IntegerField(read_only = True)
#    ivr_name = serializers.CharField(required = True,allow_blank = False, max_length = 128)
#    ivr_number = serializers.CharField(read_only = True,required = True, allow_blank = False, max_length =15)
#    ivr_updated = serializers.HiddenField(default=timezone.now)
#    datetime = serializers.CharField(default=timezone.now)
#    def create(self, validated_data):
 #       """
  #      Create and return a new `Ivr` instance, given the validated data.
   #     """
#        return Ivr.objects.create(**validated_data)

    screenshot = serializers.ImageField(required=False,allow_empty_file=True,)
    photo = serializers.ImageField(required=False,allow_empty_file=True,)
    text =  serializers.CharField(required=False,)
    class Meta:
        model = TestLog
#        fields = '__all__'
#        fields = ('id', 'screenshot', 'photo', 'datetime', 'text', 'test_id')

class TestSerializer(serializers.ModelSerializer):
    """
    Serializing Test table
    """
    class Meta:
        model = Test
        fields = '__all__'
