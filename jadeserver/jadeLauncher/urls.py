from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='News'),
    path('jadeLauncherVersion/', views.jadeLauncherVersion, name='Jade Launcher Version'),
    path('returnNews/', views.returnNews, name='Return News'),
    path('checkForExistingLauncherId/', views.checkForExistingLauncherId, name='Check for Existing Launcher ID'),
    path('updateLauncherId/', views.updateLauncherId, name='Update Launcher ID'),
    path('download/', views.download, name='Download'),
    path('downloadInstaller/', views.downloadInstaller, name='Download Installer')
    ]