from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class News(models.Model):
    code = models.CharField(max_length=12, default="0")
    head = models.CharField(max_length=200, default="Headline not specified")
    text = RichTextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    url = models.CharField(max_length=300, default="none")
    category = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return(f"[{self.code}] > {self.head} [{self.date}]")

    class Meta:
        verbose_name_plural = 'News'

class Launcher(models.Model):
    LauncherId = models.CharField(max_length=10, default="noId")
    username = models.CharField(max_length=100, default="notSignedIn")
    version = models.CharField(max_length=10, default="notUpdated")
    lastUsedDate = models.DateField(blank=True)

    def __str__(self):
        return(f"'{self.username}' using Launcher '{self.LauncherId}' on version '{self.version}'")

class Version(models.Model):
    major = models.CharField(max_length=3, default="0")
    minor = models.CharField(max_length=3, default="0")
    patch = models.CharField(max_length=3, default="0")

    def __str__(self):
        return(f"{self.major}.{self.minor}.{self.patch}")

class NewsCodes(models.Model):
    one = models.CharField(max_length=12, default=000)
    two = models.CharField(max_length=12, default=000)
    three = models.CharField(max_length=12, default=000)

    def __str__(self):
        return(f"{self.one}/{self.two}/{self.three}")

    class Meta:
        verbose_name_plural = 'News Codes'
