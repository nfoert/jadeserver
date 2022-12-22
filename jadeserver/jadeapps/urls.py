from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jadeAppsVersion/', views.jadeAppsVersion, name='jadeAppsVersion')
    ]