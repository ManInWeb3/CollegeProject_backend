#from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TestSerializer, TestLogSerializer
from .models import Test, TestLog

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views import generic

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
    try:
        curtest = Test.objects.get(pin_code=pin)
    except Test.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Such Test doesn't exist."}, status=404)

    print(request.method +" = "+ pin)
#GET get list of all avilable testlogs
    if request.method == 'GET':
        testlog = TestLog.objects.filter(test = curtest)
        serializer = TestLogSerializer(testlog, many = True)
        return JsonResponse(serializer.data, safe=False)

# POST add new testlog
    elif request.method == 'POST':
        text = request.POST.get('text')
        photo = request.FILES['photo']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        photo_url = fs.url(fs.save(photo.name, photo))
        screenshot = request.FILES['screenshot']
        screenshot_url = fs.url(fs.save(screenshot.name, screenshot))

        testcur = Test.objects.get(pin_code = pin)
        if testcur.isactive and testcur.active_from < timezone.now().date() and timezone.now().date() < testcur.active_till:
            testlogcur = TestLog(text = text, test = testcur, datetime = timezone.now(), photo = photo_url, screenshot = screenshot_url)
            testlogcur.save()
            return JsonResponse({"status": "ok", "message": "TestLog successfully added."})

        else:
            return JsonResponse({"status": "error", "message": "Thus test is not active or wrong date."}, status=499)

    else:
        return JsonResponse({"status": "error", "message": "Permission to this method is denied"}, status=499)


#@csrf_exempt
@login_required
def TestTimeLineByPIN(request,pin):
    """
    TimeLine views for TestLog by Test PIN
    only GET by PIN is available
    """
    curtest = get_object_or_404(Test, pin_code = pin)
    curtestlog = TestLog.objects.filter(test = curtest)

    return render(request, 'testlogs/timeline.html', {'test': curtest,'testlog': curtestlog})

class IndexView(generic.ListView):
    template_name = 'tests/index.html'
    context_object_name = 'tests_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Test.objects.all() #filter()
