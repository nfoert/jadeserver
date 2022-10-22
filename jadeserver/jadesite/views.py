from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    url = request.get_full_path()
    context = {
        'url': url,
    }
    return render(request, "index.html", context)
