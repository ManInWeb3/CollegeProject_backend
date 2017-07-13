from django.conf.urls import url, include
#from rest_framework import routers
from django.views.generic.base import RedirectView
from . import views
from tests.views import StudentListView, StudentCreate, StudentUpdate, StudentDelete
from tests.views import QuestionListView, QuestionCreate, QuestionUpdate, QuestionDelete
from tests.views import TestListView, TestUpdate, TestCreate, TestDelete

app_name = 'tests'
urlpatterns = [

# API endpoints
    # url(r'^api/v1/', include('tests.urls', namespace='testsapi')),
    # url(r'^tests/', include('tests.urls', namespace='testswww')),

    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^api/v1/testlog/bypin/(?P<pin>[0-9]+)/$', views.TestLogDetailViewByPIN, name = 'apitestlogbypin'),

    # url(r'^timelinebypin/(?P<pin>[0-9]+)/$', views.TestTimeLineByPIN, name = 'testlogbypin'),

    url(r'^api/v1/test/$', views.apiTestListView, name = 'apitestlist'),
    url(r'^api/v1/test/bypin/(?P<pin>[0-9]+)/$', views.apiTestDetailView, name = 'apitestdetailbypin'),  

    url(r'^testlog/$', views.TestLogListView),
    url(r'^testlog/(?P<pk>[0-9]+)/$', views.TestLogDetailView),
    url(r'^testlog/bypin/(?P<pin>[0-9]+)/$', views.TestTimeLineByPIN, name = 'testlogbypin'),

    url(r'^test/$', TestListView.as_view(), name='test-list'),
    url(r'^test/(?P<pk>[0-9]+)/$', TestUpdate.as_view(), name='test-update'),
    url(r'^test/add/$', TestCreate.as_view(), name='test-add'),
    url(r'^test/(?P<pk>[0-9]+)/delete/$', TestDelete.as_view(), name='test-delete'),    

    url(r'^student/$', StudentListView.as_view(), name='student-list'),
    url(r'^student/(?P<pk>[0-9]+)/$', StudentUpdate.as_view(), name='student-update'),
    url(r'^student/add/$', StudentCreate.as_view(), name='student-add'),
    url(r'^student/(?P<pk>[0-9]+)/delete/$', StudentDelete.as_view(), name='student-delete'),    

    url(r'^question/$', QuestionListView.as_view(), name='question-list'),
    url(r'^question/(?P<pk>[0-9]+)/$', QuestionUpdate.as_view(), name='question-update'),
    url(r'^question/add/$', QuestionCreate.as_view(), name='question-add'),
    url(r'^question/(?P<pk>[0-9]+)/delete/$', QuestionDelete.as_view(), name='question-delete'),    

    # url(r'^.*$', RedirectView.as_view(url='/login/', permanent=False))
]