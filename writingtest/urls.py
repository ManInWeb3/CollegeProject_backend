"""writingtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
#from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
#router = routers.DefaultRouter()
#router.register(r'tests', views.TestViewSet)
#router.register(r'testlogs', views.TestLogViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
#    url(r'^api/', include('tests.urls',namespace = "tests")),
    # url(r'^api/v1/', include('tests.urls', namespace='testsapi')),
    # url(r'^tests/', include('tests.urls', namespace='testswww')),
    url(r'^', include('tests.urls', namespace='testsapp')),
    url(r'^login/$', views.login, name='login'), #, kwargs={'next': '/tests/'}),
    url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': '/login/'}),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static('tests/static/media/', document_root=settings.MEDIA_ROOT)


