from django.http import HttpResponse
from jadeCore.models import Account, VerificationCode
from django.shortcuts import redirect
from django.utils import timezone
import datetime
from django.contrib.auth.hashers import make_password, check_password
import random
import pytz
import platform
utc = pytz.UTC

if platform.system() == "Linux":
    import sys
    sys.path.insert(0, '/home/nfoert/jadeserver/jadeServerUtilities/')
    import jadeServerUtilities as jsu

elif platform.system() == "Windows":
    import jadeServerUtilities.jadeServerUtilities as jsu

from trycourier import Courier

client = Courier(auth_token="pk_prod_78G758D0ZZ4VPQJN79MDWTYTHESR")

def index(request):
    return redirect("https://nofoert.wixsite.com/jade")

def create(request):
    createCurrentUrl = request.get_full_path()

    # Extract strings
    try:
        createuser = jsu.substring(createCurrentUrl, "?user=", ",password=")
        createpassword = jsu.substring(createCurrentUrl, ",password=", ",email=")
        createemail = jsu.substring(createCurrentUrl, ",email=", ",name=")
        createname = jsu.substring(createCurrentUrl, ",name=", "&")
        createname = createname.replace("%20", " ")

    except Exception as e:
        jsu.log("SERVER ERROR", f"There was a problem when substringing data out of a create account request. {e}")
        return HttpResponse("There was a problem.")

    if "user" and ",password" and ",email" and ",name" and "?" and "&" in createCurrentUrl:

        

        createCheckForExistingAccount = Account.objects.filter(userName=createuser)
        if len(createCheckForExistingAccount) == 0:


            # return HttpResponse("user="+ user + "\n \n" + "password=" + password + "\n \n" + "email="+ email + "\n \n" + "name=" + name)

            hashedPassword = make_password(createpassword)

            createAccount = Account(userName=createuser, password=hashedPassword, email=createemail, name=createname, plus="False", dateCreated=datetime.datetime.now(), suspended="no")
            createAccount.save()

            resp = client.send(
                event="jade-welcome-account",
                recipient=createname,
                profile={
                    "email": createemail,
                },
                data={
                  "recipientName": createname
                }
            )

            jsu.log("INFO", f"{createuser} created a Jade Account.")
            return HttpResponse("Account successfully created.")



        elif len(createCheckForExistingAccount) > 0:
            jsu.log("USER ERROR", f"{createuser} tried to create a Jade Account, but that Account already exists.")
            return HttpResponse("That account already exists.")


        else:
            jsu.log("SERVER ERROR", f"{createuser} tried to create a Jade Account, but there was a problem.")
            return HttpResponse("There was a problem.")



    else:
        jsu.log("LAUNCHER ERROR", f"{createuser} tried to create a Jade Account, but it's not a valid create account url.")
        return HttpResponse("JADE SERVER ERROR: Not a valid create account url")

def get(request):
    getUrl = request.get_full_path()
    if "?user" and ",password" and "?" and "&" in getUrl:

        getuser = jsu.substring(getUrl, "?user=", ",password")
        getpassword = jsu.substring(getUrl, ",password=", "&")

        getuser = getuser.replace("%0A", "")
        getpassword = getpassword.replace("%0A", "")


        try:
            getData = Account.objects.filter(userName=getuser)

        except:
            jsu.log("USER ERROR", f"{getuser} just tried to sign in, but it was an incorrect password.")
            return HttpResponse("There's no account that matches that username and password.")

        try:
            passwordCheck = check_password(getpassword, getData[0].password)

        except Exception as e:
            jsu.log("SERVER ERROR", f"{getuser} just tried to sign in, but there was a problem checking password. {e}")
            return HttpResponse("There was a problem.")
        if passwordCheck == True:

            if len(getData) == 1:
                USERNAME = getData[0].userName
                PASSWORD = getData[0].password
                EMAIL = getData[0].email
                NAME = getData[0].name
                PLUS = getData[0].plus
                SUSPENDED = getData[0].suspended

                jsu.log("INFO", f"{getuser} just signed in.")
                return HttpResponse(f"user={USERNAME},password={PASSWORD},email={EMAIL},name={NAME},plus={PLUS},suspended={SUSPENDED}&")


            elif len(getData) == 0:
                jsu.log("USER ERROR", f"{getuser} just tried to sign in, but it was an incorrect password.")
                return HttpResponse("There's no account that matches that username and password.")

            elif len(getData) > 1:
                jsu.log("SERVER ERROR", f"{getuser} just tried to sign in, but there is {len(getData)} accounts that match those credentials.")
                return HttpResponse("It looks like there's " + len(getData) + " accounts that match those credentials. We're a little bit confused over here.")

            else:
                jsu.log("SERVER ERROR", f"{getuser} hit the else statement when trying to sign in.")
                return HttpResponse("There was a problem.")

        elif passwordCheck == False:
            jsu.log("USER ERROR", f"{getuser} just tried to sign in, but it was an incorrect password.")
            return HttpResponse("There's no account that matches that username and password.")

    else:
        jsu.log("LAUNCHER ERROR", f"{getuser} had an incorrect url when signing in!")
        return HttpResponse("That's not a valid get user data url.")

def createVerificationCode(request):
    # nfoert.pythonanywhere.com/jadeCore/createVerificationCode?username=<username>,password=<password>&
    # Creates a verification code and emails it to the user.
    url = request.get_full_path()

    username = jsu.substring(url, "?username=", ",password")
    password = jsu.substring(url, "password=", "&")

    username = username.replace("%0A", "")
    password = password.replace("%0A", "")

    try:
        AccountData = Account.objects.filter(userName=username)

    except Exception as e:
            jsu.log(f"There was a problem getting Account data. {e}")
            return HttpResponse("There was a problem getting Accouunt data.")

    if len(AccountData) == 1:
        passwordCheck = check_password(password, AccountData[0].password)

        if passwordCheck == True:
            #Sign in correctly
            email = AccountData[0].email

            generatedCode = ""

            for i in range(6):
                number = random.randint(0, 9)
                number = str(number)
                generatedCode = generatedCode + number

            now = datetime.datetime.now()
            expireTime = now + datetime.timedelta(hours=1)

            verificationCode = VerificationCode(code=generatedCode,username=username,expires=expireTime)
            verificationCode.save()

            resp = client.send(
                event="jade-new-verification-code",
                recipient=username,
                profile={
                    "email": email,
                },
                data={
                  "username": username,
                  "code": generatedCode
                }
            )

            jsu.log("INFO", f"{username} just generated a verification code.")
            return HttpResponse(True)

        else:
            return HttpResponse("Your username or password is not correct.")

    else:
        return HttpResponse("There's more than one Account with that username.")



def changePassword(request):
    # nfoert.pythonanywhere.com/jadeCore/changePassword?username=<username>,password=<password>,code=<verification code>,new=<new password>&
    # Checks for a verification code, then changes the password, then removes the code.
    changePasswordUrl = request.get_full_path()
    if "?" and "&" in changePasswordUrl:
        username = jsu.substring(changePasswordUrl, "?username=", ",password")
        password = jsu.substring(changePasswordUrl, "password=", ",code")
        code = jsu.substring(changePasswordUrl, "code=", ",new")
        new = jsu.substring(changePasswordUrl, "new=", "&")

        username = username.replace("%0A", "")
        password = password.replace("%0A", "")
        new = new.replace("%0A", "")

        try:
            AccountData = Account.objects.filter(userName=username)

        except Exception as e:
            jsu.log(f"There was a problem getting Account data. {e}")
            return HttpResponse("There was a problem getting Account data.")

        try:
            CodeData = VerificationCode.objects.filter(username=username, code=code)
            now = timezone.now()
            expires = CodeData[0].expires


            if now < expires:
                jsu.log("INFO", f"{username}'s verification code is not expired.")

            else:
                jsu.log("INFO", f"{username}'s verification code is expired.")
                CodeData.delete()
                return HttpResponse("That verification code is expired.")


        except Exception as e:
            jsu.log("WARN", f"There was a problem getting Verification Code data. {e}")
            return HttpResponse("There was a problem getting Verification Code data.")


        if len(AccountData) == 1:

            passwordCheck = check_password(password, AccountData[0].password)

            if passwordCheck == True:
                if password == new:
                    jsu.log("WARN", f"{username} just tried to change their password but they tried to change it to the same password.")
                    return HttpResponse("You can't change your password to the same password it was before!")

                else:
                    if len(CodeData) == 1:
                        hashedPassword = make_password(new)
                        AccountData[0].password = hashedPassword
                        AccountData[0].save()
                        jsu.log("INFO", f"{username} just changed their password.")
                        CodeData.delete()

                        resp = client.send(
                            event="jade-password-changed",
                            recipient=AccountData[0].email,
                            profile={
                                "email": AccountData[0].email,
                            },
                            data={
                                "username": AccountData[0].userName,
                                }
                        )
                        return HttpResponse(True)

                    else:
                        jsu.log("WARN", f"{username} just tried to change their password, but their verification code was incorrect.")
                        return HttpResponse("That verification code does not exist.")

            else:
                jsu.log("WARN", f"{username} just tried to change their password, but their credentials didn't match anything in the database.")
                return HttpResponse("That username and password don't match any Account in the database.")

        else:
            jsu.log("FATAL", f"{username} just tried to change their password, but there's more than one Account with that username.")
            return HttpResponse("There's more than one account that matches that username!")



