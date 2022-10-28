from django.shortcuts import render
from django.http import HttpResponse
from jadeLauncher.models import Version, News
import platform
if platform.system() == "Linux":
    import sys
    sys.path.insert(0, '/home/nfoert/.virtualenvs/jadeserver/jadeserver/jadeserver/jadeServerUtilities')
    import jadeServerUtilities as jsu

elif platform.system() == "Windows":
    import jadeServerUtilities.jadeServerUtilities as jsu

def index(request):
    url = request.get_full_path()
    allPosts = News.objects.all()
    latestPost1 = allPosts[len(allPosts) - 1]
    latestPost2 = allPosts[len(allPosts) - 2]
    latestPost3 = allPosts[len(allPosts) - 3]
    context = {
        'latestPost1':
        {
            "code": latestPost1.code,
            "head": latestPost1.head,
            "text": latestPost1.text,
            "date": latestPost1.date,
        },
        "latestPost2":
        {
           "code": latestPost2.code,
            "head": latestPost2.head,
            "text": latestPost2.text,
            "date": latestPost2.date,
        },
        "latestPost3":
        {
           "code": latestPost3.code,
            "head": latestPost3.head,
            "text": latestPost3.text,
            "date": latestPost3.date,
        }
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

def contact(request):
    return render(request, "contact.html")

def post(request):
    url = request.get_full_path()
    if "?" and "&" in url:
        #Url is good
        codeSubstring = jsu.substring(url, "?", "&")
        try:
            postGet = News.objects.filter(code=codeSubstring)
            print(len(postGet))

        except:
            print("Post not found.")
            return False

        context = {
            "head" : postGet[0].head,
            "text" : postGet[0].text,
            "date" : postGet[0].date
        }

        return render(request, "post.html", context)
