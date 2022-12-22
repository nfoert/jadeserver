from django.http import HttpResponse
from jadeapps.models import Version
from django.shortcuts import redirect
import platform

if platform.system() == "Linux":
    import jadeServerUtilities.jadeServerUtilities as jsu

elif platform.system() == "Windows":
    import jadeServerUtilities.jadeServerUtilities as jsu

def index(request):
    return redirect("https://nofoert.wixsite.com/jade")

def jadeAppsVersion(request):
    jsu.log("INFO", "The current version of Jade Apps was just supplied to a user.")
    versionData = Version.objects.all()
    major = versionData[0].major
    minor = versionData[0].minor
    patch = versionData[0].patch
    return HttpResponse(f"major={major},minor={minor},patch={patch}&")
