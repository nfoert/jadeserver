from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("download/", views.download, name='download'),
    path("contact/", views.contact, name='contact'),
    path("post/", views.post, name='post'),
]