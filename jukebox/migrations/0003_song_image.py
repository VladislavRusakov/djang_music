# Generated by Django 4.2.7 on 2023-11-12 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jukebox', '0002_remove_song_duration_remove_song_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]