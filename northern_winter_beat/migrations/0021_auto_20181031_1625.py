# Generated by Django 2.1.1 on 2018-10-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0020_auto_20181031_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created',), 'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AlterField(
            model_name='winterbeatsettings',
            name='spotify_link',
            field=models.CharField(blank=True, help_text='If you have a link to a playlist on Spotify relevant to the festival', max_length=255, null=True, verbose_name='Link to Spotify'),
        ),
        migrations.AlterField(
            model_name='winterbeatsettings',
            name='ticket_link',
            field=models.CharField(blank=True, help_text='This link will show up as the tickets sales', max_length=255, null=True, verbose_name='Link to tickets'),
        ),
        migrations.AlterField(
            model_name='winterbeatsettings',
            name='youtube_link',
            field=models.CharField(blank=True, help_text='If you have a link to a playlist on Youtube relevant to the festival', max_length=255, null=True, verbose_name='Link to Youtube'),
        ),
    ]
