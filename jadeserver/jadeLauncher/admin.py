from django.contrib import admin
from .models import News, Launcher, Version, NewsCodes

admin.site.register(News)
admin.site.register(Launcher)
admin.site.register(Version)
admin.site.register(NewsCodes)
