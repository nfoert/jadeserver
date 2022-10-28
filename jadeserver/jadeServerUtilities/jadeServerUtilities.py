import datetime
import platform


# Logging
def log(tag, text):
    now = datetime.datetime.now()
    if platform.system() == "Linux":
        logFile = open("JadeServerLog.txt", "a")

    elif platform.system() == "Windows":
        logFile = open("./jadeServerUtilities/JadeServerLog.txt", "a")

    logFile.write(f"\n[{now.month}/{now.day}/{now.year}] [{now.hour}:{now.minute}:{now.second}] |{tag}| > {text}")
    logFile.close()

# Substringing
class SubstringError(Exception):
    pass

def substring(s, one, two):

    string = s
    try:
        start = string.find(one) + len(one)
    except:
        raise SubstringError("Unable to find the first string.")

    try:
        end = s.find(two)
    except:
        raise SubstringError("Unable to find the second string.")

    result = s[start:end]
    print("Jade Substringer: " + str(result))

    log("INFO", "Just subsringed.")

    return result
