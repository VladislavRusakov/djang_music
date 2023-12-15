from itertools import cycle
import random
import time
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from jukebox import models

from pygame import mixer
from mutagen.mp3 import MP3
import shout


def icecast_connect():
    """Connecting to icecast server
    using credentials below"""
    shoutobj = shout.Shout()
    shoutobj.host = '10.15.15.57'
    shoutobj.port = 8000
    shoutobj.user = 'source'
    shoutobj.password = 'ChangeMe'
    shoutobj.mount = "/spaces"
    shoutobj.format ='mp3'
    shoutobj.open()

    return shoutobj


def index_view(request):
    """Renders index page with playlist and queue data"""
    # songs = models.Song.objects.all

    playlist = 'friday_night'
    # playliststack = {}
    # for stack in models.PlaylistStack.objects.all().select_related('playlist_id', 'song_id'):
    #     if stack.playlist_id not in playliststack:
    #         playliststack[stack.playlist_id] = []
    #         playliststack[stack.playlist_id].append(stack.song_id)
    #     else:
    #         playliststack[stack.playlist_id].append(stack.song_id)

    # print(playliststack)
    playliststack = models.PlaylistStack.objects.all().select_related('playlist_id', 'song_id').filter(playlist_id__name=playlist)
    queue = models.Queue.objects.all()

    context = {
        "title": "Playlist",
        "playlist": playlist,
        "playliststack": playliststack,
        "queue": queue,
    }

    return render(request, 'jukebox/index.html', context=context)


def play_playlist_view(request):
    """Launches a playlist locally"""
    playlist_name = 'friday_night'
    playliststack = models.PlaylistStack.objects.all().select_related('playlist_id', 'song_id').filter(playlist_id__name=playlist_name)

    song_stack = []
    for song in playliststack:
        file = f"media/{song.song_id.audio_file}"
        song_stack.append(file)
    run_playlist(song_stack)

    return redirect('')


def run_playlist(playlist: list) -> None:
    """Checks for requested songs in queue
    Plays songs in system with mixer"""
    for path in playlist:
        oldest_request = models.Queue.objects.first()
        if not oldest_request:
            mixer.init()
            mixer.music.load(path)
            mixer.music.play()
            mixer.music.set_volume(0.7)
            time.sleep(MP3(path).info.length)
        else:
            path = f'''media/{oldest_request.song_id.audio_file}'''
            mixer.init()
            mixer.music.load(path)
            mixer.music.play()
            mixer.music.set_volume(0.7)
            time.sleep(MP3(path).info.length)

            models.Queue.objects.filter(song_id=oldest_request.song_id).delete()


def stream_song(song_path) -> None:
    """Opens mp3 file and streams in to icecast"""
    shoutobj = icecast_connect()

    total = 0
    with open (song_path, 'rb') as f:
        nbuffer = f.read(4096)
        while True:
            buffer = nbuffer
            nbuffer = f.read(4096)
            total += len(buffer)
            if len(buffer) == 0:
                break
            shoutobj.send(buffer)
            shoutobj.sync()
        f.close()
    shoutobj.close()


def stream_playlist_view(request):
    """Launches a playlist stream"""
    if request.method == 'POST':
        playlist_name = 'friday_night'
        playliststack = models.PlaylistStack.objects.all().select_related('playlist_id', 'song_id').filter(playlist_id__name=playlist_name)

        song_stack = []
        for song in playliststack:
            file = f"media/{song.song_id.audio_file}"
            song_stack.append(file)
        stream_playlist(song_stack)


def stream_playlist(playlist: list, runs=1) -> None:
    """Gets a list of songs paths
    and streams them in a cycle"""
    def looper(playlist, runs):
        path = cycle(playlist)
        for _ in range(runs):
            oldest_request = models.Queue.objects.first()

            if not oldest_request:
                stream_song(next(path))
            else:
                request_path = f'''media/{oldest_request.song_id.audio_file}'''
                stream_song(request_path)

                models.Queue.objects.filter(song_id=oldest_request.song_id).delete()

    # for path in playlist:
    #     oldest_request = models.Queue.objects.first()

    #     if not oldest_request:
    #         stream_song(path)
    #     else:
    #         path = f'''media/{oldest_request.song_id.audio_file}'''
    #         stream_song(path)

    #         models.Queue.objects.filter(song_id=oldest_request.song_id).delete()
    looper(playlist, runs)

    return redirect('')


def song_list_view(request):
    """"""
    songs = models.Song.objects.all

    context = {
        "title": "Playlist",
        "songs": songs,
    }

    return render(request, 'jukebox/songs_list.html', context=context)


def add_song_by_request(request):
    """"""
    if request.method == 'POST':
        models.Queue.objects.create(song_id_id=request.POST.get('song'))

    return HttpResponseRedirect("/songs")
