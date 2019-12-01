from rest_framework import routers
from django.conf.urls import url, include
from .views import sample_api, word_to_pdf

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^sample_api', sample_api),
    url(r'^convert/word_to_pdf', word_to_pdf)
]
