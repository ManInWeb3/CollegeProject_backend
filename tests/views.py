#from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import generic
from django.urls import reverse_lazy

from .serializers import TestSerializer, TestLogSerializer
from .models import Student, Test, TestLog, Question

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# ================= API ======================

@csrf_exempt
def apiTestListView(request):
    """
    List Test.
    """
    if request.method == 'GET':
        testset = Test.objects.all()
        serializer = TestSerializer(testset, many=True)
#        print(serializer.data.student)
#        serializer.data.student
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def apiTestDetail(request,pin):
    """
    Detail views for Test
    only GET by PIN code is available
    """
    try:
        test = Test.objects.get(pin_code=pin)
    except Test.DoesNotExist:
        return JsonResponse({'status': 'error','message': 'no such element'},status=404)

    if request.method == 'GET':
        serializer = TestSerializer(test)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def TestLogDetailView(request,pk):
    """
    Detail views for Test
    only GET by ID and POST are available
    """
    try:
        testlog = TestLog.objects.get(pk=pk)
    except TestLog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TestLogSerializer(testlog)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def apiTestLogDetailViewByPIN(request,pin):
    """
    Detail views for TestLog by Test PIN
    only GET by ID and POST are available
    """
    # print( int(pin) )
    try:
        curtest = Test.objects.get(pin_code=int(pin) )
    except Test.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Such Test doesn't exist. PIN: "+pin}, status=404)

#    print(request.method +" = "+ pin)
# GET get list of all avilable testlogs by the pin
    if request.method == 'GET':
        testlog = TestLog.objects.filter(test = curtest)
        serializer = TestLogSerializer(testlog, many = True)
        return JsonResponse(serializer.data, safe=False)

# POST add new testlog to test with the pin
    elif request.method == 'POST':

        if curtest.isactive():
            text = request.POST.get('text')
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            try:
                photo = request.FILES['photo']
                photo_url = fs.url(fs.save(photo.name, photo))
            except KeyError:
                photo_url = "/tests/static/media/NOWEBCAM.png"

            screenshot = request.FILES['screenshot']
            screenshot_url = fs.url(fs.save(screenshot.name, screenshot))

            testlogcur = TestLog(text = text, test = curtest, datetime = timezone.now(), photo = photo_url, screenshot = screenshot_url)
            testlogcur.save()

#            print("@@@@@@@"+text)
            curtest.answer_text = text
            curtest.date_passed = timezone.now()
            curtest.save()

            return JsonResponse({"status": "ok", "message": "TestLog successfully added.", "resttime": curtest.resttime})

        else:
            return JsonResponse({"status": "error", "message": "Test is not active,passed or test's time is up.", "resttime": curtest.resttime}, status=499)

    else:
        return JsonResponse({"status": "error", "message": "Permission to this method is denied"}, status=499)

#@csrf_exempt
#def TestLogListView(request):
#    """
#    List TestLog, or create a new one.
#    """
#    if request.method == 'GET':
#        testlogset = TestLog.objects.all()
#        serializer = TestLogSerializer(testlogset, many=True)
#        return JsonResponse(serializer.data, safe=False)


# ===================== TestLogs ======================
#@csrf_exempt
@login_required
def TestLogDetailByPIN(request,pin):
    """
    TimeLine views for TestLog by Test PIN
    only GET by PIN is available
    """
    curtest = get_object_or_404(Test, pin_code = pin)
    curtestlog = TestLog.objects.filter(test = curtest)

    return render(request, 'tests/timeline.html', {'test': curtest,'testlog': curtestlog})


#============= CRUD Test ==========================

@method_decorator(login_required, name='dispatch')
class TestListView(ListView):
    model = Test
    fields = ['active_from', 'active_till', 'duration', 'student', 'question']

    def get_queryset(self):
        return Test.objects.filter(created_by = self.request.user)

@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    fields = ['active_from', 'active_till', 'duration', 'student', 'question']

@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    fields = ['student', 'question', 'duration', 'active_from', 'active_till']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TestCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TestDelete(DeleteView):
    '''
    Need to check is it an empty test???
    we cannot delete a test if there are any TestLogs

    '''
    model = Test
    success_url = reverse_lazy('tests:test-list')


@method_decorator(login_required, name='dispatch')
class TestCheck(UpdateView):
    model = Test
    fields = ['answer_marked', 'grade']
    template_name = 'tests/test_check.html'



#============== CRUD Student ====================

@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    fields = ['first_name','last_name', 'student_dob','passport_num','passport_scan','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name','last_name', 'student_dob','passport_num','passport_scan','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentCreate(CreateView):
    model = Student
    fields = ['first_name','last_name', 'student_dob','passport_num','passport_scan','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('tests:student-list')


#============= CRUD Question ==========================

@method_decorator(login_required, name='dispatch')
class QuestionListView(ListView):
    model = Question
    fields = ['question_name', 'question_text','question_type','duration']

@method_decorator(login_required, name='dispatch')
class QuestionUpdate(UpdateView):
    model = Question
    fields = ['question_name', 'question_text','question_type','duration']

@method_decorator(login_required, name='dispatch')
class QuestionCreate(CreateView):
    model = Question
    fields = ['question_name', 'question_text','question_type','duration']

@method_decorator(login_required, name='dispatch')
class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('tests:question-list')

@method_decorator(login_required, name='dispatch')
class QuestionDetail(DetailView):
    model = Question
    fields = ['question_name', 'question_text','question_type']


