from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jadeAssistantVersion/', views.jadeAssistantVersion, name='jadeAssistantVersion')
    ]