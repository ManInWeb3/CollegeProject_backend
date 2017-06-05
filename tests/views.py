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
from .models import Student, Test, TestLog

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

@csrf_exempt
def TestListView(request):
    """
    List Test.
    """
    if request.method == 'GET':
        testset = Test.objects.all()
        serializer = TestSerializer(testset, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def TestDetailView(request,pin):
    """
    Detail views for Test
    only GET by PIN code is available
    """
    try:
        test = Test.objects.get(pin_code=pin)
    except Test.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TestSerializer(test)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def TestLogListView(request):
    """
    List TestLog, or create a new one.
    """
    if request.method == 'GET':
        testlogset = TestLog.objects.all()
        serializer = TestLogSerializer(testlogset, many=True)
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
def TestLogDetailViewByPIN(request,pin):
    """
    Detail views for TestLog by Test PIN
    only GET by ID and POST are available
    """
    # print( int(pin) )
    try:
        curtest = Test.objects.get(pin_code=int(pin) )
    except Test.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Such Test doesn't exist. PIN: "+pin}, status=404)

    print(request.method +" = "+ pin)
#GET get list of all avilable testlogs
    if request.method == 'GET':
        testlog = TestLog.objects.filter(test = curtest)
        serializer = TestLogSerializer(testlog, many = True)
        return JsonResponse(serializer.data, safe=False)

# POST add new testlog
    elif request.method == 'POST':
        testcur = Test.objects.get(pin_code = pin)
        if testcur.isactive():
            text = request.POST.get('text')
            photo = request.FILES['photo']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            photo_url = fs.url(fs.save(photo.name, photo))
            screenshot = request.FILES['screenshot']
            screenshot_url = fs.url(fs.save(screenshot.name, screenshot))

            testlogcur = TestLog(text = text, test = testcur, datetime = timezone.now(), photo = photo_url, screenshot = screenshot_url)
            testlogcur.save()
            return JsonResponse({"status": "ok", "message": "TestLog successfully added."})

        else:
            return JsonResponse({"status": "error", "message": "Test is not active or wrong date."}, status=499)

    else:
        return JsonResponse({"status": "error", "message": "Permission to this method is denied"}, status=499)


#@csrf_exempt
@login_required
# @method_decorator(login_required, name='dispatch')
def TestTimeLineByPIN(request,pin):
    """
    TimeLine views for TestLog by Test PIN
    only GET by PIN is available
    """
    curtest = get_object_or_404(Test, pin_code = pin)
    curtestlog = TestLog.objects.filter(test = curtest)

    return render(request, 'tests/timeline.html', {'test': curtest,'testlog': curtestlog})

@method_decorator(login_required, name='dispatch')
class TestListView(ListView):
    model = Test
    fields = ['pin_code','topic','active_from','active_till','date_passed', 'student']
 
    def get_queryset(self):
        return Test.objects.filter(created_by = self.request.user)
    

@method_decorator(login_required, name='dispatch')
class TestUpdate(UpdateView):
    model = Test
    fields = ['topic','active_from','active_till', 'student']

@method_decorator(login_required, name='dispatch')
class TestCreate(CreateView):
    model = Test
    fields = ['topic','active_from','active_till', 'student']

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
class StudentListView(ListView):
    model = Student
    fields = ['first_name','last_name','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name','last_name','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentCreate(CreateView):
    model = Student
    fields = ['first_name','last_name','email','skype']

@method_decorator(login_required, name='dispatch')
class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('tests:student-list')
