from django.db import models
# import hashlib
import math
from random import randint
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
import datetime

#import random
#import string

import uuid
import os

class Student(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default = 1)
    first_name = models.CharField(max_length = 100)
    last_name  = models.CharField(max_length = 100)
    student_dob = models.DateField('Students DoB', default='2000-01-01', blank=True)

    passport_num  = models.CharField(max_length = 20, default=0, blank=True)
    passport_scan = models.ImageField(blank=True)

    email = models.CharField(max_length = 100, blank=True)
    skype = models.CharField(max_length = 50, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('tests:student-list', kwargs={})

class QuestionType(models.Model):
    type_name = models.CharField(max_length = 50, default='')
    type_blank = RichTextField(config_name='default')

    def __str__(self):
        return self.type_name

def upload_attachments(instance, filename):
    now = timezone.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'attachments/{}_{}{}'.format(
        now.strftime("%Y/%m/%d/%Y%m%d%H%M%S"),
        str(uuid.uuid4())[:7],
        filename_ext.lower()
    )

class Attachment(models.Model):
    name = models.CharField(max_length=100)
    path = models.FileField(upload_to=upload_attachments)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('tests:attachment-list', kwargs={})    

class Question(models.Model):
    question_name = models.CharField(max_length = 50, default='')
    question_text = RichTextField(config_name='default')
    duration = models.IntegerField(default = 40)
    question_type = models.ForeignKey( QuestionType, on_delete = models.PROTECT, default =1 )
    attachments = models.ManyToManyField( Attachment, blank = True)

    def __str__(self):
        return self.question_name
    def get_absolute_url(self):
        return reverse('tests:question-list', kwargs={})    


class Test(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default = 1)
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    pin_code = models.IntegerField(editable = False,default=0)  #Default 30 min
    duration = models.IntegerField(default=40)  #Default 30 min
    date_created = models.DateTimeField('date created', auto_now_add=True, editable = False)
    active_from = models.DateField('active from')
    active_till = models.DateField('active till')
    date_passed = models.DateTimeField('date passed', null=True, blank=True, editable = False)

    question = models.ForeignKey(Question, on_delete = models.PROTECT, default = 1)
    question_text = RichTextField(blank=True)

    answer_text   = models.TextField(blank=True,null=True)
    answer_marked = RichTextField(blank=True, config_name='marking')

#    teacher_notes = RichTextField(blank=True)
    grade = models.DecimalField(max_digits=2, decimal_places=1,default = 0)

#    @property
    def get_attachments(self):
#        return self.question.attachment
        return Attachment.objects.filter(question = self.question)

    @property
    def question_type(self):
        return self.question.question_type.__str__

    @property
    def resttime(self):
# NOW is between date from and date till
# Check if the duration > first test_log and NOW
        FirstTL = TestLog.objects.filter(test = self).order_by('datetime').first()

        if FirstTL :
            FirstTestLogDateTime = FirstTL.datetime
            TestLogDURATION = timezone.now()-FirstTL.datetime
            rest_time = self.duration - TestLogDURATION.seconds/60
            print("Test resttime: "+str(rest_time))
            return math.ceil(rest_time)
        else :
            print("The test doesn't start")
            return self.duration

    def isactive(self):
        print(self.date_passed)
        return self.active_from <= timezone.now().date() <= self.active_till and 0 <= self.resttime and self.date_passed is None

    def iseditable(self):
        return not bool(TestLog.objects.filter(test = self).count())

    def save(self, *args, **kwargs):
        if self.iseditable() :
            print("EDIT="+str(self.iseditable()))
            if( self.pin_code == 0 ):
                while True:
                    npin = randint(100000000,999999999)
                    #Check that the NUMBER is not already used as PIN
                    try:
                        curtest = Test.objects.get(pin_code=npin)
                    except Test.DoesNotExist:
                        self.pin_code = npin
                        break

    #Need to check if the question was changed
            self.question_text = self.question.question_text
            self.duration = self.question.duration
            self.answer_text = self.question.question_type.type_blank
        super(Test, self).save(*args, **kwargs)

    def __str__(self):
        return self.question.question_name+": "+self.student.first_name + " " +self.student.last_name
    def get_absolute_url(self):
        return reverse('tests:test-list', kwargs={})

def get_testlogs_path(instance, filename):
    return os.path.join( 'media', str(instance.test.pin_code), filename)

class TestLog(models.Model):
    test    = models.ForeignKey(Test, on_delete = models.PROTECT, editable = False)
    datetime= models.DateTimeField(auto_now_add=True, blank=True, editable = False)
    info    = models.CharField(max_length = 50, default='', blank=True, editable = False)
    text    = models.TextField(blank=True,null=True)
    screenshot = models.ImageField(upload_to=get_testlogs_path, editable = False,blank=True, null=True)
    photo   = models.ImageField( upload_to=get_testlogs_path, editable = False)








