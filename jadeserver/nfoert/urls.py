from django.urls import path

from nfoert import views

app_name = "nfoert"
urlpatterns = [
    path('', views.index, name='index'),
    path("allposts/", views.allposts, name='allposts'),
    path("post/", views.post, name='post')
]