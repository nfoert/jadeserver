from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("allposts/", views.allposts, name='allposts'),
    path("post/", views.post, name='post')
]