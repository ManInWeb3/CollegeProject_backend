from django.contrib import admin

# Register your models here.
from .models import Student
from .models import Question
from .models import Test
from .models import TestLog

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestLog)


class TestLogAdmin(admin.ModelAdmin):
    readonly_fields = ('text',)

