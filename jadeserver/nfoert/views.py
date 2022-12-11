from django.shortcuts import render
from nfoert.models import Post
import platform
if platform.system() == "Linux":
    import jadeServerUtilities.jadeServerUtilities as jsu

elif platform.system() == "Windows":
    import jadeServerUtilities.jadeServerUtilities as jsu


def index(request):
    url = request.get_full_path()
    allPosts = Post.objects.all()
    latestPost1 = allPosts[len(allPosts) - 1]
    latestPost2 = allPosts[len(allPosts) - 2]
    latestPost3 = allPosts[len(allPosts) - 3]
    context = {
        "post1": {
            "code": latestPost1.code,
            "head": latestPost1.head,
            "date": latestPost1.date,
            "text": latestPost1.text,
        },
        "post2": {
            "code": latestPost2.code,
            "head": latestPost2.head,
            "date": latestPost2.date,
            "text": latestPost2.text,
        },
        "post3": {
            "code": latestPost3.code,
            "head": latestPost3.head,
            "date": latestPost3.date,
            "text": latestPost3.text,
        }
    }

    return render(request, "nfoert/index.html", context)

def allposts(request):
    url = request.get_full_path()
    if "?" and "&" in url:
        categorySubstring = jsu.substring(url, "?category=", "&")

        newsGet = Post.objects.filter(category=categorySubstring).exclude(category='hidden').order_by("date").reverse()

        context = {
            "post" : newsGet
        }
        return render(request, "nfoert/allposts.html", context)

    else:
        newsGet = Post.objects.all().exclude(category='hidden').order_by("date").reverse()

        context = {
            "post" : newsGet
        }
        return render(request, "nfoert/allposts.html", context)

def post(request):
    url = request.get_full_path()
    if "?" and "&" in url:
        #Url is good
        codeSubstring = jsu.substring(url, "?", "&")
        postGet = Post.objects.filter(code=codeSubstring)
        print(len(postGet))
        print(len(postGet) >= 1)



        if postGet.exists():
            context = {
                "head" : postGet[0].head,
                "text" : postGet[0].text,
                "date" : postGet[0].date
            }

            return render(request, "nfoert/post.html", context)

        else:
            context = {
                "head" : "404 post not found",
                "text" : "",
                "date" : ""
            }
            return render(request, "nfoert/post.html", context)


