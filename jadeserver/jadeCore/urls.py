from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('get/', views.get, name='get'),
    path('changePassword/', views.changePassword, name='Change Password'),
    path("createVerificationCode/", views.createVerificationCode, name="Create Verification Code")
    ]