from django.conf.urls import url, include
#from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'ivr', views.IvrList)
#router.register(r'ivrmenu', views.IvrMenuViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
#urlpatterns = [
#    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#]

app_name = 'tests'
urlpatterns = [
#    url(r'^testlog/$', views.TestLogListView),
#    url(r'^ivr/(?P<pk>[0-9]+)/$', views.IvrDetailView),
    url(r'^timelinebpin/(?P<pin>[^/]+)$', views.TestTimeLineByPIN, name = 'testlogbypin'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^test/$', views.TestListView),
    url(r'^test/(?P<pin>[^/]+)$', views.TestDetailView),
    url(r'^testlog/$', views.TestLogListView),
    url(r'^testlog/(?P<pk>[0-9]+)/$', views.TestLogDetailView),
    url(r'^testlog/bypin/(?P<pin>[^/]+)$', views.TestLogDetailViewByPIN),
]