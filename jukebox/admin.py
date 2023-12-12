from django.contrib import admin
from jukebox import models

# Register your models here.
admin.site.register(models.Song)
admin.site.register(models.Playlist)
admin.site.register(models.PlaylistStack)
admin.site.register(models.Queue)