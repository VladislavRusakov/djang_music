from django.db import models


class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="image")
    audio_file = models.FileField(blank=True, null=True, upload_to="song")
    # audio_link = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class PlaylistStack(models.Model):
    song_id = models.ForeignKey(to=Song, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(to=Playlist, on_delete=models.CASCADE)

class Queue(models.Model):
    song_id = models.ForeignKey(to=Song, on_delete=models.CASCADE)