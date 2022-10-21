from django.urls import path

from . import views

urlpatterns = [path('jadeLauncherVersion/', views.jadeLauncherVersion, name='Jade Launcher Version')]

