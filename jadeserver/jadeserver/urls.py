"""jadeserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('jade/', include('jade.urls')),
    path('jadeCore/', include('jadeCore.urls')),
    path('jadeAssistant/', include('jadeAssistant.urls')),
    path('jadeLauncher/', include('jadeLauncher.urls')),
    path('jadeapps/', include('jadeapps.urls')),
    path('jadesite/', include('jadesite.urls', namespace='jadesite')),
    path('nfoert/', include('nfoert.urls', namespace='nfoert')),
    path('admin/', admin.site.urls)

]
