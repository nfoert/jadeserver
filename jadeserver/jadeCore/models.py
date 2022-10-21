from django.db import models

class Account(models.Model):
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=10000)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    plus = models.CharField(max_length=5, default="False")
    #YYYY-MM-DD
    dateCreated = models.DateField(blank=True)
    suspended = models.CharField(default="no", max_length=9999)
    notes = models.TextField(max_length=999999, default="noNotes")

    def __str__(self):
         return(self.userName)

class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    username = models.CharField(max_length=100)
    expires = models.DateTimeField(blank=True)
