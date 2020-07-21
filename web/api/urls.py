from django.conf.urls import url, include
from rest_framework import routers

from .views import healthcheck, convert

router = routers.DefaultRouter()

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^healthcheck/$", healthcheck),
    url(r"^convert/(?P<converter_class>\w+)/to/(?P<extension_to>\w+)/$", convert),
]
