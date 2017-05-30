from django.contrib import admin

# Register your models here.
from .models import Student
from .models import Teacher
from .models import Test
from .models import TestLog

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Test)
admin.site.register(TestLog)


class TestLogAdmin(admin.ModelAdmin):
    readonly_fields = ('text',)

