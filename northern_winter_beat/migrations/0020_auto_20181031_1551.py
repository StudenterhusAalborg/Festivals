# Generated by Django 2.1.1 on 2018-10-31 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0019_artist_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='winterbeatsettings',
            name='spotify_link',
            field=models.CharField(help_text='If you have a link to a playlist on Spotify relevant to the festival', max_length=255, null=True, verbose_name='Link to Spotify'),
        ),
        migrations.AddField(
            model_name='winterbeatsettings',
            name='ticket_link',
            field=models.CharField(help_text='This link will show up as the tickets sales', max_length=255, null=True, verbose_name='Link to tickets'),
        ),
        migrations.AddField(
            model_name='winterbeatsettings',
            name='youtube_link',
            field=models.CharField(help_text='If you have a link to a playlist on Youtube relevant to the festival', max_length=255, null=True, verbose_name='Link to Youtube'),
        ),
    ]
