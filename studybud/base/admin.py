from django.contrib import admin
from base import models

admin.site.register(models.User)
admin.site.register(models.Room)
admin.site.register(models.Topic)
admin.site.register(models.Message)
