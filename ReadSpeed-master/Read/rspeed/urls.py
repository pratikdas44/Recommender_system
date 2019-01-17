from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rspeed import views

from django.views.generic.base import RedirectView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'rspeed', views.ReadSpeedViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', RedirectView.as_view(url='reg')),
    url(r'^reg$', views.ReadSpeedCreate.as_view(), name='reg'),
    url(r'^done/(?P<pk>[0-9]+)$', views.home, name='done'),
]
