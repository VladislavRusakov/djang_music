# Generated by Django 4.2.7 on 2023-11-12 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jukebox', '0003_song_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playliststack',
            name='playlist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jukebox.playlist'),
        ),
    ]