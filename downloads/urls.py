from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authservice/', views.authservice, name='authservice'),
    re_path(r'^device/(?P<pk>\d+)/$', views.device, name='device'),
    re_path(r'^downloader/(?P<pk>\d+)/$', views.downloadprovider, name='downloader'),
]
