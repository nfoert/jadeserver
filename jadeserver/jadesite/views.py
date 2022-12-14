from django.shortcuts import render
from django.http import HttpResponse
from jadeLauncher.models import Version, News
import platform
if platform.system() == "Linux":
    import jadeServerUtilities.jadeServerUtilities as jsu

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
    return render(request, "jadesite/index.html", context)

def download(request):
    versionData = Version.objects.all()
    major = versionData[0].major
    minor = versionData[0].minor
    patch = versionData[0].patch
    context = {
        "version": f"{major}.{minor}.{patch}",
    }
    return render(request, "jadesite/download.html", context)

def contact(request):
    return render(request, "jadesite/contact.html")

def post(request):
    url = request.get_full_path()
    if "?" and "&" in url:
        #Url is good
        codeSubstring = jsu.substring(url, "?", "&")
        postGet = News.objects.filter(code=codeSubstring)
        print(len(postGet))
        print(len(postGet) >= 1)
        
        

        if postGet.exists():
            context = {
                "head" : postGet[0].head,
                "text" : postGet[0].text,
                "date" : postGet[0].date
            }

            return render(request, "jadesite/post.html", context)

        else:
            context = {
                "head" : "404 post not found",
                "text" : "",
                "date" : ""
            }
            return render(request, "jadesite/post.html", context)

def allposts(request):
    url = request.get_full_path()
    if "?" and "&" in url:
        categorySubstring = jsu.substring(url, "?category=", "&")
        
        newsGet = News.objects.filter(category=categorySubstring).exclude(category='hidden').order_by("date").reverse()
    
        context = {
            "news" : newsGet
        }
        return render(request, "jadesite/allposts.html", context)

    else:
        newsGet = News.objects.all().exclude(category='hidden').order_by("date").reverse()
    
        context = {
            "news" : newsGet
        }
        return render(request, "jadesite/allposts.html", context)
        
