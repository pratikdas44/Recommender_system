from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    url('rspeed/', include("rspeed.urls")),
    url('^$', RedirectView.as_view(url='rspeed/')),
]
