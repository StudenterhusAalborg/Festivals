# Generated by Django 2.1.1 on 2018-12-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0024_auto_20181127_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='winterbeatsettings',
            name='show_timeline',
            field=models.BooleanField(default=False, help_text='Show the page with the date each artist is going to play', verbose_name='Show timeline'),
        ),
    ]
