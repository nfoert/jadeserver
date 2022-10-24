from django.shortcuts import render
from django.http import HttpResponse
from jadeLauncher.models import Version

def index(request):
    url = request.get_full_path()
    context = {
        'url': url,
    }
    return render(request, "index.html", context)

def download(request):
    versionData = Version.objects.all()
    major = versionData[0].major
    minor = versionData[0].minor
    patch = versionData[0].patch
    context = {
        "version": f"{major}.{minor}.{patch}",
    }
    return render(request, "download.html", context)