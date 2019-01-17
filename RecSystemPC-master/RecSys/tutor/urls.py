from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from tutor import views

from django.views.generic.base import RedirectView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'teacherfeedback', views.TeacherFeedbackViewSet)
router.register(r'teacher', views.TeacherViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', RedirectView.as_view(url='reg')),
    url(r'^reg$', views.TeacherFeedbackCreate.as_view(), name='reg'),
    url(r'^sim$', views.sim_teacher, name='sim'),
    url(r'^sim_r$', views.sim_res, name='sim_r'),
    url(r'^done/(?P<pk>[0-9]+)$', views.home, name='done'),
]
