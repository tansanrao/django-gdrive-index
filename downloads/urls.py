from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authservice/', views.authservice, name='authservice'),
    re_path(r'^device/(?P<pk>\d+)/$', views.device, name='device'),
    path('api/', views.api, name='api'),
]
