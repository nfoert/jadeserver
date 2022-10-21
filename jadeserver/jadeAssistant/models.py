from django.db import models

class Version(models.Model):
    major = models.CharField(max_length=1,default=0)
    minor = models.CharField(max_length=1,default=0)
    patch = models.CharField(max_length=1,default=0)

    def __str__(self):
        return(f"{self.major}.{self.minor}.{self.patch}")
