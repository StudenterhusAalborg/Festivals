# Generated by Django 2.1.1 on 2018-12-01 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0025_winterbeatsettings_show_timeline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='date',
        ),
        migrations.AddField(
            model_name='artist',
            name='concert_date',
            field=models.DateField(blank=True, help_text='The day the artist is going to play', null=True, verbose_name='concert date'),
        ),
    ]
