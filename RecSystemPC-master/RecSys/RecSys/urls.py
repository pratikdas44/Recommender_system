from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    url('tutor/', include("tutor.urls")),
    url('^$', RedirectView.as_view(url='tutor/')),
]
