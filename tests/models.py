from django.db import models
import hashlib
from random import randint
# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    skype = models.CharField(max_length = 50)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Teacher(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    skype = models.CharField(max_length = 50)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Test(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete = models.PROTECT)
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    topic   = models.TextField()
    pin_code = models.CharField(max_length = 32, editable = False)
    duration = models.IntegerField(default=1800)  #Default 30 min
    date_created = models.DateTimeField('date created', auto_now_add=True, editable = False)
    isactive = models.BooleanField(default = False)
    active_from = models.DateField('active from', null=True, blank=True)
    active_till = models.DateField('active till', null=True, blank=True)
    date_passed = models.DateTimeField('date passed', null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if( len(self.pin_code) == 0 ):
            self.pin_code = hashlib.md5(str(self.id).encode('utf-8') + str(randint(1000,9999)).encode('utf-8') + str(self.teacher).encode('utf-8')).hexdigest()
        super(Test, self).save(*args, **kwargs)

    def __str__(self):
        return self.teacher.first_name +" "+  self.teacher.last_name + " - " + self.student.first_name + " " +self.student.last_name


class TestLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True, editable = False)
    text = models.TextField(blank=True,null=True)
    test = models.ForeignKey(Test, on_delete = models.PROTECT, editable = False)
    screenshot = models.ImageField(upload_to='media/', editable = False, blank=True, null=True)
    photo = models.ImageField(upload_to='media/', editable = False)








