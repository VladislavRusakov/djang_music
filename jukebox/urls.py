from django.urls import path
from jukebox import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('play', views.play_playlist_view, name='play'),
    path('songs', views.song_list_view, name='songs'),
    path('request', views.add_song_by_request, name='request'),
    path('startstream', views.stream_playlist_view, name='startstream')
]
