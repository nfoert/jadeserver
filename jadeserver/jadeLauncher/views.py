from django.http import HttpResponse, FileResponse
from jadeLauncher.models import News, Launcher, Version, NewsCodes
from django.shortcuts import redirect
import platform

import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

if platform.system() == "Linux":
    import sys
    sys.path.insert(0, '/home/nfoert/jadeserver/jadeServerUtilities/')
    import jadeServerUtilities as jsu

elif platform.system() == "Windows":
    import jadeServerUtilities.jadeServerUtilities as jsu

def index(request):
    return redirect("https://nofoert.wixsite.com/jade")

def news(request):
    NewsUrl = request.get_full_path()
    NewsUrl = NewsUrl.replace("%0A", "")
    if "?" in NewsUrl:


        Code = jsu.substring(NewsUrl, "?", "&")

        #Code = NewsUrl.replace(r"https://nfoert.pythonanywhere.com/jade/news?", "")
        print("Jade News: Code is: " + Code)
        newsData = News.objects.filter(code=Code)
        if len(newsData) == 0:
            print("There is no news article that matches that code.")
            return HttpResponse("There is no news article that matches that code.")

        elif len(newsData) == 1:
            HEAD = newsData[0].head
            TEXT = newsData[0].text
            DATE = newsData[0].date
            URL = newsData[0].url

            newsString = f"header={HEAD},text={TEXT},date={DATE},url={URL}&"
            jsu.log("INFO", f"News data was just supplied for code {Code}")
            return HttpResponse(newsString)

        elif len(newsData) > 1:
            print("There's more than one news article that matches that code.")
            jsu.log("SERVER ERROR", "There's more than one news article that matches that code.")
            return HttpResponse("There's more than one news article that matches that code.")


def jadeLauncherVersion(request):
    versionData = Version.objects.all()
    major = versionData[0].major
    minor = versionData[0].minor
    patch = versionData[0].patch
    jsu.log("INFO", "A user just requested the current version of the Jade Launcher.")
    return HttpResponse(f"major={major},minor={minor},patch={patch}&")

def returnNews(request):
    newsCodesData = NewsCodes.objects.all()
    news1 = newsCodesData[0].one
    news2 = newsCodesData[0].two
    news3 = newsCodesData[0].three
    jsu.log("INFO", "A user just requested the current news codes for the Launcher.")
    return HttpResponse(f"1={news1},2={news2},3={news3}&")

def checkForExistingLauncherId(request):
    checkForExistingLauncherIdUrl = request.get_full_path()
    IdInput = jsu.substring(checkForExistingLauncherIdUrl, "?", "&")

    LauncherIds = Launcher.objects.filter(LauncherId=IdInput)



    if len(IdInput) > 10:
        print("That input is larger than 10 characters.")
        jsu.log("ID ERROR", f"{IdInput} was just checked for a valid Id. It's larger than 10.")
        return HttpResponse("LARGER THAN 10")

    elif len(IdInput) < 10:
        print("That input is less then 10 characters.")
        jsu.log("ID ERROR", f"{IdInput} was just checked for a valid Id. It's smaller than 10.")
        return HttpResponse("LESS THAN 10")

    elif len(LauncherIds) == 0:
        print("There are no ids that match the inputted one.")
        jsu.log("INFO", f"{IdInput} is safe to use. Will create a Launcher Id for it.")
        createLauncherId = Launcher(LauncherId=IdInput, username="notSignedIn", version="notUpdated", lastUsedDate=timezone.now())
        createLauncherId.save()
        return HttpResponse("SAFE TO USE")

    else:
        print("That id already exists.")
        jsu.log("INFO", f"{IdInput} Already exists.")
        return HttpResponse("ALREDY EXISTS")

def updateLauncherId(request):
    updateLauncherIdUrl = request.get_full_path()
    if "?" and "&" in updateLauncherIdUrl:
        print("Url is good. Updating status.")

        id = jsu.substring(updateLauncherIdUrl, "?id=", ",username")
        username = jsu.substring(updateLauncherIdUrl, ",username=", ",version")
        version = jsu.substring(updateLauncherIdUrl, ",version=", "&")

        username.replace("%0A", "")

        if len(id) == 10:
            print("Id is proper length. Can now update status.")

            try:
                idData = Launcher.objects.get(LauncherId=id)

            except:
                print("No id exists. Will make one.")
                try:
                    createId = Launcher(LauncherId=id, username=username, version=version, lastUsedDate=timezone.now())
                    createId.save()
                    jsu.log("INFO", "{username} just updated their Launcher ID, but needed to create an entry in the server.")
                    return HttpResponse("DONE")

                except Exception as e:
                    print(f"There was a problem updating launcher status. {username} needed to create a new Id in the server, but {e}")
                    jsu.log("ID ERROR", f"{username} needed to create a new Id in the server, but '{e}'")

            try:
                idData.username = username
                idData.version = version
                idData.lastUsedDate = timezone.now()
                idData.save()
                print("Done.")
                jsu.log("INFO", f"{username} just updated their Launcher Id status successfully.")
                return HttpResponse("DONE")

            except Exception as e:
                print(f"There was a problem setting id data. {e}")
                jsu.log("ID ERROR", f"There was a problem setting id data. {e}")
                return HttpResponse("PROBLEM")



        elif len(id) > 10:
            print("Id length is greater than 10.")
            jsu.log("ID ERROR", "Id length is greater than 10.")
            return HttpResponse("GREATER THAN 10")

        elif len(id) < 10:
            print("Id length is less than 10.")
            jsu.log("ID ERROR", "Id length is less than 10.")
            return HttpResponse("LESS THAN 10")

        else:
            print(f"There was a problem. id='{id}'")
            jsu.log("ID ERROR", f"There was a problem. id='{id}'")
            return HttpResponse("PROBLEM")


    else:
        print("Url is not good.")
        jsu.log("LAUNCHER ERROR", "Url is not good when updating Launcher Id status.")
        return HttpResponse("BAD URL")

def download(request):
    downloadUrl = request.get_full_path()
    if "?" and "&" in downloadUrl:
        wm = jsu.substring(downloadUrl, "?", "&")
        if wm == "Windows":
            jsu.log("INFO", "Someone just downloaded the Launcher for Windows!")
            return redirect("https://www.dropbox.com/s/0vqag0hks2bwafe/Jade%20Launcher.exe?dl=1")

        elif wm == "Mac":
            jsu.log("INFO", "Someone just downloaded the Launcher for Mac!")
            return redirect("https://www.dropbox.com/s/0lkbjia5z6wnyxi/Jade%20Launcher.zip?dl=1")

        else:
            jsu.log("DOWNLOAD ERROR", "There was a problem downloading Jade Launcher. OS={wm}")
            return HttpResponse("PROBLEM DETERMING OS")

    else:
        return HttpResponse("INVALID URL")

def downloadInstaller(request):
    downloadUrl = request.get_full_path()
    if "?" and "&" in downloadUrl:
        wm = jsu.substring(downloadUrl, "?", "&")
        if wm == "Windows":
            jsu.log("INFO", "Someone just downloaded the Launcher's Installer for Windows!")
            return redirect("https://www.dropbox.com/s/4tr6tm17iu1g4kg/Jade%20Launcher%20Installer.exe?dl=1")

        elif wm == "Mac":
            jsu.log("INFO", "Someone just downloaded the Launcher's Installer for Mac!")
            return redirect("https://www.dropbox.com/s/0d6ft4a13w9g48l/Jade%20Launcher.pkg?dl=1")

        else:
            jsu.log("DOWNLOAD ERROR", "There was a problem downloading Jade Launcher. OS={wm}")
            return HttpResponse("PROBLEM DETERMING OS")

    else:
        return HttpResponse("INVALID URL")










