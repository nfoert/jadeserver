from django.urls import path

from jadesite import views

app_name = "jadesite"
urlpatterns = [
    path('', views.index, name='index'),
    path("download/", views.download, name='download'),
    path("contact/", views.contact, name='contact'),
    path("post/", views.post, name='post'),
    path("allposts/", views.allposts, name='allposts'),
]