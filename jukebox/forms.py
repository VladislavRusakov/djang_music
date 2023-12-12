from django.forms import ModelForm

from jukebox import models


class SongRequestForm(ModelForm):

    class Meta:
        model = models.Queue
        fields = ('song_id',)
