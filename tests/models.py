from django.db import models
# import hashlib
from random import randint
from django.utils import timezone

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
#    pin_code = models.CharField(max_length = 32, editable = False)
    pin_code = models.IntegerField(editable = False,default=0)  #Default 30 min
    duration = models.IntegerField(default=1800)  #Default 30 min
    date_created = models.DateTimeField('date created', auto_now_add=True, editable = False)
#    isactive = models.BooleanField(default = False)
    active_from = models.DateField('active from')
    active_till = models.DateField('active till')
    date_passed = models.DateTimeField('date passed', null=True, blank=True, editable = False)

    def isactive(self):
        # print(timezone.now().date())
        return self.active_from <= timezone.now().date() and timezone.now().date() <= self.active_till and self.date_passed == None

    def save(self, *args, **kwargs):
        if( self.pin_code == 0 ):
            while True:
                npin = randint(100000000,999999999)
                #Check that the NUMBER is not already used as PIN
                try:
                    curtest = Test.objects.get(pin_code=npin)
                except Test.DoesNotExist:
                    self.pin_code = npin
                    break
        super(Test, self).save(*args, **kwargs)

    def __str__(self):
        return self.teacher.first_name +" "+  self.teacher.last_name + " - " + self.student.first_name + " " +self.student.last_name


class TestLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True, editable = False)
    text = models.TextField(blank=True,null=True)
    test = models.ForeignKey(Test, on_delete = models.PROTECT, editable = False)
    screenshot = models.ImageField(upload_to='media/', editable = False, blank=True, null=True)
    photo = models.ImageField(upload_to='media/', editable = False)








