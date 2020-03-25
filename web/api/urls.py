from rest_framework import routers
from django.conf.urls import url, include

from .views import sample_api, convert

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^sample_api/$', sample_api),
    url(r'^convert/(?P<converter_class>\w+)/to/(?P<extension_to>\w+)/$', convert)
]
