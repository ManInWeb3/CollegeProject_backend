from rest_framework import serializers
from .models import TestLog, Test, Attachment
import datetime
from django.utils import timezone


class TestLogSerializer(serializers.ModelSerializer):
    """
    Serializing testlog table
    """
    # screenshot = serializers.ImageField(required=False,allow_empty_file=True,)
    # photo = serializers.ImageField(required=False,allow_empty_file=True,)
    # text =  serializers.CharField(required=False,)
    datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TestLog
#        fields = '__all__'
        exclude = ('id', 'test')

class AttachmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attachment
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    """
    Serializing Test table
    """
#    queryset = Attachment.objects.all()
    attachments = AttachmentSerializer(source='get_attachments', many=True, required = False)

    student = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='first_name'
     )
    question = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='question_text'
     )

    class Meta:
        model = Test
#        fields = '__all__'
        fields = ('student', 'question', 'question_type', 'pin_code', 'duration', 'active_from', 'active_till', 'date_passed', 'resttime', 'answer_text', 'attachments')



