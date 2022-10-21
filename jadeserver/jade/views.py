from django.http import HttpResponse

# Create your views here.

def jadeLauncherVersion(request):
    major = "0"
    minor = "0"
    patch = "7"
    return HttpResponse(f"major={major},minor={minor},patch={patch}&")