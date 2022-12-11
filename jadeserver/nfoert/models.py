from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class Post(models.Model):
    code = models.CharField(max_length=100, default="0")
    head = models.CharField(max_length=500, default="no headline")
    text = RichTextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return(f"[{self.code}] > {self.head} [{self.date}]")

    class Meta:
        verbose_name_plural = 'Posts'